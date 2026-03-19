#!/bin/bash
set -e
python ../src/plugins/dynamic_xml_config/main_generate.py user_config.yaml
roslaunch sim_env main.launch
