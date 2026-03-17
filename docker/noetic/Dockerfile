# Use the official ROS Noetic base image
FROM osrf/ros:noetic-desktop-full

# Set the working directory
WORKDIR /project

SHELL ["/bin/bash", "-c"]

# Install additional dependencies if needed
RUN apt-get update --fix-missing\
    && apt-get -y --no-install-recommends install \
    git \
    gcc \
    vim \
    psmisc \
    libxml2-dev \
    libxslt-dev \
    python3 \
    python3-pip \ 
    python-is-python3\
    ros-noetic-amcl \
    ros-noetic-base-local-planner \
    ros-noetic-map-server \
    ros-noetic-move-base \
    ros-noetic-navfn \
    xvfb \
    bc \
    && rm -rf /var/lib/apt/lists/*

# python packages (benchmark dependencies)
RUN pip3 install setuptools \
    && pip3 install catkin-tools \
    && pip3 install conan==1.59.0 \
    && pip3 install numpy Pillow scipy pandas pyyaml matplotlib

# bash
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Copy the project into the container
COPY . /project

# catkin build
RUN source /opt/ros/noetic/setup.bash && cd /project/scripts && bash ./build.sh
RUN chmod +x /project/scripts/*.sh /project/docker/noetic/docker_entrypoint.sh

ENTRYPOINT ["/project/docker/noetic/docker_entrypoint.sh"]