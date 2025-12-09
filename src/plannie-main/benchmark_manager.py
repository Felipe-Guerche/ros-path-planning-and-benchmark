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
        
        # Publishers
        self.vis_pub = rospy.Publisher('/benchmark_goal', PoseStamped, queue_size=1)
        
        # Subscribers
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
        # Start Benchmark
        rospy.sleep(1.0)
        self.start_benchmark()
        
    def start_benchmark(self):
        rospy.loginfo(f"Starting benchmark for planner: {self.planner_name}")
        self.is_running = True
        self.start_time = time.time()
        
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
        self.cpu_usages.append(psutil.cpu_percent())
        self.mem_usages.append(psutil.virtual_memory().percent)
            
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

if __name__ == '__main__':
    try:
        BenchmarkManager()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
