import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List
from flowlauncher import FlowLauncher
from terminal_config_launcher import TerminalConfigLauncher

logger = logging.getLogger(__name__)


class TerminalLauncher(FlowLauncher):
    def __init__(self, plugindir: Path):
        self.configs_dir = plugindir / "configs"
        self.configs_dir.mkdir(exist_ok=True)
        self._load_available_configs()
        super().__init__()

    def _load_available_configs(self):
        self.available_configs = {}
        for config_file in self.configs_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    name = config.get('name', config_file.stem)
                    self.available_configs[name] = config_file
            except Exception as e:
                logger.exception(f"Error loading {config_file}: {e}")

    def query(self, query: str) -> List[Dict]:
        if not query:
            return [
                {
                    "Title": f"Launch: {name}",
                    "SubTitle": f"Launch terminal with {name} configuration",
                    "IcoPath": "Images/app.png",
                    'ContextData': [
                        str(config_path)
                    ],
                    "JsonRPCAction": {
                        "method": "launch_config",
                        "parameters": [str(config_path), False]
                    }
                }
                for name, config_path in self.available_configs.items()
            ]
        else:
            filtered = [
                {
                    "Title": f"Launch: {name}",
                    "SubTitle": f"Launch terminal with {name} configuration",
                    "IcoPath": "Images/app.png",
                    'ContextData': [
                        str(config_path)
                    ],
                    "JsonRPCAction": {
                        "method": "launch_config",
                        "parameters": [str(config_path), False]
                    }
                }
                for name, config_path in self.available_configs.items()
                if query.lower() in name.lower()
            ]

            if filtered:
                return filtered

            return [
                {
                    "Title": f"Create profile: {query.lower()}",
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": "create_config",
                        "parameters": [str(query.lower())],
                    },
                }]

    def launch_config(self, config_path: str, attach: bool = False):
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)

            launcher = TerminalConfigLauncher(config, attach)
            launcher.launch()

        except Exception as e:
            logger.exception(f"Error launching configuration: {e}")

    def create_config(self, config_name):
        new_config_path = self.configs_dir / f"{config_name}.yaml"
        if not new_config_path.exists():
            config = {
                "name": f"{config_name}",
                "description": "Generated through flow launcher",
                "window": {
                    "tabs": [
                        {
                            "profile": "PowerShell",
                            "directory": str(self.configs_dir),
                            "splits": [
                                {
                                    "direction": "vertical",
                                    "size": 0.5,
                                },
                                {
                                    "direction": "horizontal",
                                    "size": 0.3,
                                },
                            ]
                        },
                    ]
                },
            }
            with open(new_config_path, "w") as yaml_file:
                yaml.dump(config, yaml_file)

        else:
            logger.info("This file already exists")

    def context_menu(self, data):
        return [
            {
                "title": "Attach to Existing Window",
                "SubTitle": "Launch terminal in existing window",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "launch_config",
                    "parameters": [data[0], True]
                }
            },
            {
                "title": "Open configs directory",
                "SubTitle": "Open the folder containing terminal configurations",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_configs_dir",
                    "parameters": []
                }
            },
        ]

    def open_configs_dir(self):
        os.startfile(self.configs_dir)
