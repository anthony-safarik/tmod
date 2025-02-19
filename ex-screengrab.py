import examples
import examples.discoverfiles #file has to be explicitly imported if not specified in __init__
THIS_DESKTOP = examples.THIS_DESKTOP
THIS_COMPUTER = examples.THIS_COMPUTER

if __name__ == "__main__":
    # simple user input example to discover screen grabs on the desktop
    user_response = input(f"Would you like to check all the user desktops on {THIS_COMPUTER} for screen grabs? (y/n): ").lower() == "y"
    if user_response == True:
        fpaths = examples.discover_files(f'/Users/*/Desktop/Screen*')
        # we would need to call the discover_files explicitly if it's not imported in __init__
        # fpaths = examples.discoverfiles.discover_files(f'/Users/*/Desktop/Screen*')
        for x in fpaths: print(x)