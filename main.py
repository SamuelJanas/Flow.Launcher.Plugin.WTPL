import sys
from pathlib import Path

plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

from plugin import TerminalLauncher

if __name__ == "__main__":
    TerminalLauncher(plugindir)
