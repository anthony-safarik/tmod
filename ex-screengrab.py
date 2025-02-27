import os
import examples
import examples.discoverfiles #file has to be explicitly imported if not specified in __init__
import examples.discoverfolders
from examples.userchoice import get_user_choice
from examples.rcopy import rcopy

THIS_DESKTOP = examples.THIS_DESKTOP
THIS_COMPUTER = examples.THIS_COMPUTER


if __name__ == "__main__":
    # simple example to discover screen grabs on the desktop

    # get the xfer folders from a list
    xfer_folders = examples.discover_folders('/Volumes/*/XFER')
    this_xfer = get_user_choice(xfer_folders)

    # we would need to call the discover_files explicitly if it's not imported in __init__
    screengrabs = examples.discover_files(f'/Users/*/Desktop/Screen*')
    for x in screengrabs: print(x)

    # using input to get a true/false from y/n response
    if this_xfer:
        user_response = input(f"Would you like to move all these screen granbs from {THIS_COMPUTER} to {this_xfer}? (y/n): ").lower() == "y"
        if user_response:
            # Iterate screengrabs
            print('Moving files...')
            for src in screengrabs:
                fname = os.path.basename(src)
                dst_folder = os.path.join(this_xfer, THIS_COMPUTER, 'Desktop')
                dst = os.path.join(dst_folder, fname)

                # Make folder if needed
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                    
                # If folder exists, move the file
                if os.path.exists(dst_folder):
                    print(src, '--->' ,dst)
                    flags = ['-a', '--verbose', '--remove-source-files']
                    rcopy(src, dst, flags)
                
        else:
            print('Exiting now')
    else: print('There is no XFER folder to move these files to.')