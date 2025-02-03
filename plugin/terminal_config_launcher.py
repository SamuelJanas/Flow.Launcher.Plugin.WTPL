import logging
import subprocess
from typing import Dict

logger = logging.getLogger(__name__)

class TerminalConfigLauncher:
    def __init__(self, config: Dict, attach: bool):
        self.config = config
        self.attach = attach
    
    def launch(self):
        try:
            window_config = self.config.get('window', {})
            tabs = window_config.get('tabs', [])
            
            cmd = ['wt']
            
            if self.attach:
                cmd.append('-w 0')
            else:
                cmd.append('-w -1')
            
            for i, tab in enumerate(tabs):
                if i > 0:
                    cmd.append(';')
                    cmd.append('new-tab')
                
                if 'title' in tab:
                    cmd.append(f'--title "{tab["title"]}"')
                
                tab_profile = tab.get('profile', "PowerShell")
                cmd.append(f'-p "{tab_profile}"')
                
                tab_directory = tab.get('directory')
                if tab_directory:
                    cmd.append(f'-d "{tab_directory}"')

                tab_command = tab.get('command')
                if tab_command:
                    cmd.append(f'powershell -Command "{tab_command}"')
                
                splits = tab.get('splits', [])
                for j, split in enumerate(splits):
                    cmd.append(';')
                    
                    # Determine split direction
                    split_type = 'split-pane' if split.get('direction') == 'vertical' else 'split-pane -H'
                    cmd.append(split_type)
                    
                    split_profile = split.get('profile', tab_profile)
                    cmd.append(f'-p "{split_profile}"')
                    
                    split_directory = split.get('directory', tab_directory)
                    if split_directory:
                        cmd.append(f'-d "{split_directory}"')
                    
                    split_size = split.get('size')
                    if split_size:
                        cmd.append(f'-s {split_size}')

                    split_command = split.get('command')
                    if split_command:
                            cmd.append(f'powershell -Command "{split_command}"')
                    
            
            command = ' '.join(cmd)
            logger.info(f"Launching terminal with command: {command}")
            subprocess.Popen(command, shell=True)
        
        except Exception as e:
            logger.error(f"Error launching terminal: {e}")
            raise
