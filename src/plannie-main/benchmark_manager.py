#!/usr/bin/env python3
import rospy
import time
import psutil
import math
import os
import actionlib
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String

class BenchmarkManager:
    def __init__(self):
        rospy.init_node('benchmark_manager')
        
        # Parameters
        self.output_dir = rospy.get_param('~output_dir', './results')
        self.planner_name = rospy.get_param('~planner_name', 'unknown')
        self.goal_x = rospy.get_param('~goal_x', 2.0)
        self.goal_y = rospy.get_param('~goal_y', 2.0)
        
        # State
        self.start_time = None
        self.total_distance = 0.0
        self.last_pos = None
        self.trajectory = []
        self.cpu_usages = []
        self.mem_usages = []
        self.is_running = False
        self.finished = False
        
        # Action Client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        self.client.wait_for_server()
        rospy.loginfo("Connected to move_base server")
        
        # Move Base Process
        self.move_base_proc = self.find_move_base_process()
        if not self.move_base_proc:
            rospy.logwarn("Could not find move_base process! Resource monitoring will be system-wide.")
        
        # Publishers
        self.vis_pub = rospy.Publisher('/benchmark_goal', PoseStamped, queue_size=1)
        
        # Subscribers
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        # Synchronized Start
        target_time = rospy.get_param('~target_startup_time', 0.0)
        if target_time > 0:
            self.wait_for_sim_time(target_time)
        
        # Start Benchmark
        rospy.sleep(1.0)
        self.start_benchmark()
        
    def find_move_base_process(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # check name or cmdline
                if proc.info['name'] == 'move_base':
                    return proc
                # sometimes it's a python script wrapper or similar, but move_base is usually C++
                # check cmdline for 'move_base'
                if proc.info['cmdline'] and any('move_base' in arg for arg in proc.info['cmdline']):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def wait_for_sim_time(self, target_time):
        rospy.loginfo(f"Waiting for simulation time to reach {target_time}s...")
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            current_time = rospy.Time.now().to_sec()
            if current_time >= target_time:
                rospy.loginfo(f"Target time reached! (Current: {current_time:.2f}s)")
                break
            # Warn if we are close to timeout or something? No, just wait.
            rate.sleep()
        
    def start_benchmark(self):
        rospy.loginfo(f"Starting benchmark for planner: {self.planner_name}")
        self.is_running = True
        self.start_time = time.time()
        
        # Reset process CPU interval
        if self.move_base_proc:
            self.move_base_proc.cpu_percent(interval=None)

        # Create Goal Object
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = "map"
        goal_pose.header.stamp = rospy.Time.now()
        goal_pose.pose.position.x = self.goal_x
        goal_pose.pose.position.y = self.goal_y
        goal_pose.pose.orientation.w = 1.0
        
        # Publish for Visualization (Rviz)
        self.vis_pub.publish(goal_pose)
        
        # Send to Action Server
        goal = MoveBaseGoal()
        goal.target_pose = goal_pose
        
        self.client.send_goal(goal, done_cb=self.done_callback)
        rospy.loginfo(f"Goal sent: ({self.goal_x}, {self.goal_y})")

    def done_callback(self, status, result):
        if not self.finished:
            rospy.loginfo(f"Move base finished with status: {status}")
            success = (status == 3) # 3 is SUCCEEDED
            self.finish_benchmark(success)

    def odom_callback(self, msg):
        if not self.is_running or self.finished:
            return
            
        # Position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        current_pos = (x, y)
        
        # Distance calculation
        if self.last_pos:
            dist = math.sqrt((x - self.last_pos[0])**2 + (y - self.last_pos[1])**2)
            self.total_distance += dist
            
        self.last_pos = current_pos
        self.trajectory.append(current_pos)
        
        # Resource Monitoring
        if self.move_base_proc:
            try:
                # CPU percent for specific process (non-blocking if interval=None after first call)
                self.cpu_usages.append(self.move_base_proc.cpu_percent(interval=None))
                # Memory percent of the process
                self.mem_usages.append(self.move_base_proc.memory_percent())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.cpu_usages.append(0.0)
                self.mem_usages.append(0.0)
        else:
            # Fallback to system-wide if not found
            self.cpu_usages.append(psutil.cpu_percent())
            self.mem_usages.append(psutil.virtual_memory().percent)

        # Force Success Check (Fallback for picky move_base)
        # Calculate distance to GOAL (final target), not just path integration
        dist_to_goal = math.sqrt((x - self.goal_x)**2 + (y - self.goal_y)**2)
        
        # Force Success Check (Fallback for picky move_base)
        # Calculate distance to GOAL (final target), not just path integration
        dist_to_goal = math.sqrt((x - self.goal_x)**2 + (y - self.goal_y)**2)
        
        # Tolerance: 0.1m (10cm radius) - Stricter as requested
        # If we are close enough, declare victory.
        if dist_to_goal < 0.10:
            rospy.loginfo(f"Vehicle is within 0.10m of goal ({dist_to_goal:.3f}m). Forcing SUCCESS.")
            self.client.cancel_all_goals()
            self.finish_benchmark(True)
            return

        # Timeout Check
        # Check against a max_timeout param (default 180s = 3 mins)
        max_timeout = rospy.get_param('~max_timeout', 180.0)
        if (time.time() - self.start_time) > max_timeout:
            rospy.logwarn(f"Benchmark timed out after {max_timeout}s!")
            self.client.cancel_all_goals()
            self.finish_benchmark(False)

    def finish_benchmark(self, success):
        self.finished = True
        end_time = time.time()
        duration = end_time - self.start_time
        
        rospy.loginfo(f"Benchmark finished! Success: {success}")
        self.save_results(success, duration)
        rospy.signal_shutdown("Benchmark Complete")

    def save_results(self, success, duration):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{self.planner_name}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        avg_cpu = sum(self.cpu_usages) / len(self.cpu_usages) if self.cpu_usages else 0
        max_mem = max(self.mem_usages) if self.mem_usages else 0
        
        with open(filepath, 'w') as f:
            f.write(f"Planner: {self.planner_name}\n")
            f.write(f"Status: {'SUCCESS' if success else 'FAILURE'}\n")
            f.write(f"Time: {duration:.4f} s\n")
            f.write(f"Distance: {self.total_distance:.4f} m\n")
            f.write(f"Avg CPU: {avg_cpu:.2f} %\n")
            f.write(f"Max Mem: {max_mem:.2f} %\n")
            f.write("Trajectory:\n")
            for p in self.trajectory:
                f.write(f"{p[0]}, {p[1]}\n")
                
        rospy.loginfo(f"Results saved to {filepath}")

        # Save to unified summary if configured
        summary_file = rospy.get_param('~summary_file', '')
        if summary_file:
            self.save_to_summary(summary_file, success, duration, self.total_distance, avg_cpu, max_mem)

    def save_to_summary(self, filepath, success, time_taken, total_dist, avg_cpu, max_mem):
        file_exists = os.path.isfile(filepath)
        try:
            with open(filepath, 'a') as f:
                if not file_exists:
                    # Header matches run_battery.sh: Scenario,GlobalPlanner,LocalPlanner,Status,Time(s),Distance(m),CPU(%),Memory(%)
                    f.write("Scenario,GlobalPlanner,LocalPlanner,Status,Time(s),Distance(m),CPU(%),Memory(%)\n")
                
                status_str = "SUCCESS" if success else "FAILURE"
                
                # Split planner_name (e.g., "static_hybrid_astar_dwa") into components
                # Assumption: scenario is first, local is last. Middle is global (can have underscores).
                parts = self.planner_name.split('_')
                if len(parts) >= 3:
                    scenario = parts[0]
                    local = parts[-1]
                    global_p = "_".join(parts[1:-1])
                    f.write(f"{scenario},{global_p},{local},{status_str},{time_taken:.4f},{total_dist:.4f},{avg_cpu:.2f},{max_mem:.2f}\n")
                else:
                    # Fallback for manual single runs or unexpected formats
                    f.write(f"{self.planner_name},,{status_str},{time_taken:.4f},{total_dist:.4f},{avg_cpu:.2f},{max_mem:.2f}\n")
                    
                rospy.loginfo(f"Added to summary: {filepath}")
        except Exception as e:
            rospy.logerr(f"Failed to write to summary file: {e}")

    def shutdown_hook(self):
        pass # Placeholder for any cleanup if needed

if __name__ == '__main__':
    try:
        manager = BenchmarkManager()
        rospy.on_shutdown(manager.shutdown_hook)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
