from .computername import get_computer_name
from .discoverfolders import discover_folders

THIS_COMPUTER = get_computer_name()
THIS_DESKTOP = discover_folders("/Users/*/Desktop")
THIS_DOWNLOADS = discover_folders("/Users/*/Downloads")
THIS_XFER = discover_folders("/Volumes/*/XFER")