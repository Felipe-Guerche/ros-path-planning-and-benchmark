#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
******************************************************************************************
*  Copyright (C) 2023 Yang Haodong, All Rights Reserved                                  *
*                                                                                        *
*  @brief    generate launch file dynamicly based on user configure.                     *
*  @author   Haodong Yang                                                                *
*  @version  1.0.3                                                                       *
*  @date     2023.07.19                                                                  *
*  @license  GNU General Public License (GPL)                                            *
******************************************************************************************
"""
import os
import xml.etree.ElementTree as ET
from plugins import ObstacleGenerator, PedGenerator, RobotGenerator, MapsGenerator, XMLGenerator


class MainGenerator(XMLGenerator):
    def __init__(self, *plugins) -> None:
        super().__init__()
        self.app_list = [app for app in plugins]

    def writeMainLaunch(self, path):
        """
        Create configure file of package `sim_env` dynamically.

        Args:
            path (str): the path of file(.launch.xml) to write.
        """
        # Check headless mode from environment
        is_headless = os.environ.get("BENCHMARK_HEADLESS", "0") == "1"

        # root
        launch = MainGenerator.createElement("launch")

        # other applications
        for app in self.app_list:
            assert isinstance(app, XMLGenerator), "Expected type of app is XMLGenerator"
            app_register = app.plugin()
            for app_element in app_register:
                launch.append(app_element)

        # Determine rviz_file (disable in headless mode)
        rviz_file = "" if is_headless else self.user_cfg["rviz_file"]

        # include
        include = MainGenerator.createElement("include", props={"file": "$(find sim_env)/launch/config.launch"})
        include.append(MainGenerator.createElement("arg", props={"name": "world", "value": "$(arg world_parameter)"}))
        include.append(MainGenerator.createElement("arg", props={"name": "map", "value": self.user_cfg["map"]}))
        include.append(MainGenerator.createElement("arg", props={"name": "robot_number", "value": str(len(self.user_cfg["robots_config"]))}))
        include.append(MainGenerator.createElement("arg", props={"name": "rviz_file", "value": rviz_file}))

        # Headless overrides
        if is_headless:
            include.append(MainGenerator.createElement("arg", props={"name": "gui", "value": "false"}))
            include.append(MainGenerator.createElement("arg", props={"name": "headless", "value": "true"}))

        launch.append(include)
        MainGenerator.indent(launch)

        with open(path, "wb+") as f:
            ET.ElementTree(launch).write(f, encoding="utf-8", xml_declaration=True)

    def plugin(self):
        pass


# dynamic generator
main_gen = MainGenerator(PedGenerator(), RobotGenerator(), ObstacleGenerator(), MapsGenerator())
main_gen.writeMainLaunch(main_gen.root_path + "sim_env/launch/main.launch")

