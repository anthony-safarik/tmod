from .computername import get_computer_name
from .discoverfolders import discover_folders
# functions from files in the package can't be used directly without line below
from .discoverfiles import discover_files

THIS_COMPUTER = get_computer_name().split('.')[0] #sometimes the computer name appears with appended ".local" text
THIS_DESKTOP = discover_folders("/Users/*/Desktop") #set var to list of desktops