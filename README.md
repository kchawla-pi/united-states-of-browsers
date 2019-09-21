[![Build Status](https://circleci.com/gh/kchawla-pi/united-states-of-browsers.svg?branch=master)](https://circleci.com/gh/kchawla-pi/united-states-of-browsers)
[![Build Status](https://dev.azure.com/kchawla-pi/united-states-of-browsers/_apis/build/status/kchawla-pi.united-states-of-browsers?branchName=master)](https://dev.azure.com/kchawla-pi/united-states-of-browsers/_build/latest?definitionId=1&branchName=master)
[![Build Status](https://codecov.io/gh/kchawla-pi/united-states-of-browsers/branch/master/graph/badge.svg)](https://codecov.io/gh/kchawla-pi/united-states-of-browsers)



# United States of Browsers
##### A project to combine and organize history and bookmarks across multiple browsers and browser profiles.

*The wiki has more info about the project's philosophy.*

I use multiple browsers and multiple browser profiles. This scatters my history, bookmarks across multiple interfaces. 

Whenever I wish to search something, I have to go through them all until I find them. I wish to build a tool which will read browser profile files and combine the history and bookmarks list, ready to be searched and organized automatically.

Initial idea is to read the broswer's sqlite3 database files and copy and combine the data in one place, then allow simultaneous keyword and date range search on it. More features for searching and organization and maybe an ML algo to recommend from within the combined history and the web will be implemented.

Note: Play with it, I haven't made it Demo-ready yet.
It shouldn't damage anything, but if it is does...
THIS IS A USE AT YOUR OWN RISK SOFTWARE.

###### Installation instructions are further down.

 - Built with python3.6
 - using Pycharm 2017.3 CE
 - On Windows 10 x64 Fall Creators Update
 - For Mozilla Firefox, Chrome, Opera, Vivaldi
 - May work with other Windows versions.

It is Windows ~ONLY~ for now. I got it working with my personal installation of Linux Mint. Watch this space.

Easy to make it work for other OSes.
Changing path locations for browser profile folder should make it work on other OS. (TODO)

Following functionality has been implemented as of Jan 30, 2018:
 - Browser histories of Firefox, Chrome, Opera and Vivaldi can be combined into one database.
 - A web UI served by Flask.
 - Keyword and Date range search.
  
  
Future Plans:  
 - Update duplicate entries. (?)
 - Refine the GUI using JS & AJAX.
 - Scraping the URL and getting the text back.
 - ML to pick out keywords from text and title.
 - Use that to tag and categorize the history entries

##### To Check it out: (Currently, instructions for command line only)

0. Install the required software if it is not already installed.  
     - Install python 3.6 for windows x64 from https://www.python.org/downloads/release/python-363/.
     During setup, choose to add python to the PATH variable, if it is not already chosen by default.
     - Install git from https://git-scm.com/downloads.
1. Open terminal (In windows, these are cmd.exe and powershell).
2. Navigate to the directory/folder where you wish to store the files.
     In this example, we will do this on the windows Desktop.
     In the terminal window, type the command:

        cd C:\Users\<your username>\Desktop (press ENTER).
3. Clone this repo's `master` branch using the command:

        git clone "https://github.com/kchawla-pi/united-states-of-browsers.git"
4. Navigate into the newly created directory/folder:

        cd united-states-of-browsers
5. Make a virtual environment using:

        python -m venv venv
6. Activate the virtual environment:

        venv\Scripts\activate
7. Install the required python packages:

        pip install -r requirements.txt
8. Install the project:

        pip install .
      or if you wanna play with the code;
        
        pip install --editable .
        
9. To merge the databases and launch the user interface, run:

        python .\united_states_of_browsers\run_usb.py

10. Then go to your browser of choice and visit:

        localhost:5000
11. To stop, go back to the same terminal window  where the program is running and press `Ctrl+C`.
12. Deactivate the virtual environment by typing `deactivate` and pressing ENTER.

Merging the database will generate an sqlite file in the `~\USB\` directory/folder, where `~` is the user directory/folder.  
In windows this is typically `C:\Users\<user name>`

Currently tests are not available.

To run tests (requires pytest), type:

    pytest

