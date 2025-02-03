# Windows Terminal Profile Launcher

## Overview 

Windows Terminal Profile Launcher (WTPL) is a Flow.Launcher Plugin using YAML configuration for faster launch of predefined windows terminal workspace profiles.

## Usage

Plugin uses the `wtp` keyword. Use context menu to attach a profile into an existing terminal window. 
setup `.yaml` files do define workspaces.

### Example YAML configuration

```yaml
description: Example yaml config
name: example
window:
  tabs:
  - title: "Main Tab"  # (optional) Title of the tab
    directory: "%USERPROFILE%"  # (optional) Starting directory
    profile: "PowerShell"  # (optional) Terminal profile to use
    command: "nvim"  # (optional) Command to execute (uses PowerShell -Command)
    splits:
    - direction: vertical  # Split pane direction: vertical or horizontal
      size: 0.5  # (optional) Size ratio of the split
      profile: "Command Prompt"  # (optional) Profile for the split pane
      directory: "C:\\foo\\bar"  # (optional) Working directory for the split
    - direction: horizontal
      size: 0.3
```

Directories not specified by splits by default inherit from tabs.
