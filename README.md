# united-states-of-browsers
A project to combine &amp; organize history and bookmarks across multiple browsers and browser profiles.



 - Built with python3.6
 - using Pycharm 2017.2.3 CE
 - On Windows 10 x64 Creators Update
 - For Mozilla Firefox.
 - May work with other Windows versions.

Does not support other OS and browsers YET. Easy to make it work for other OSes.
Changing path locations for Mozilla profile folder should make it work on other OS. (TODO)

Following functionality has been implemented as of Nov 17, 2017:
 - The merging firefox browser history databases functionality has been implemented.
 - Search using python functions, but not using the UI.
 - Rudminetary UI to view the first 1000 entries running on a local webserver.

##### To Run:
1. Clone this repo's `frontend` branch,  or download and unzip it.
2. Navigate to the directory/folder where it has been cloned.

To merge the databases, run:

    $py .\united_states_of_browsers\db_merge\merge_browser_databases.py

To launch the user interface, run:

    $py .\united_states_of_browsers\usb_server\usb_server.py
    Then go to the browser and visit: localhost:5000

Merging the database will generate an sqlite file in the \united_states_of_browsers directory/folder, 'all_merged.sqlite' .
A url_hash_log.bin _might_ also be generated. It is a binary file containing the hashes of URLs that were written to 'merged_fx_db.sqlite'.

To run tests (requires pytest), type:
$pytest

The project idea is, essentially, I use multiple browsers and multiple browser profiles. This scatters my history, bookmarks across multiple interfaces. 

Whenever I wish to search something, I have to go through them all until I find them. I wish to build a tool which will read browser profile files and combine the history and bookmarks list, ready to be searched and organized automatically.

Initial idea is to read the broswer's sqlite3 database files and copy and combine the data in one place, maybe a json. More features for searching and organization and maybe an ML algo to recommend from within the combined history and the web will be implemented.

Note: Play with it, I haven't made it Demo-ready yet.
It shouldn't damage anything, but if it is does...
THIS IS A USE AT YOUR OWN RISK SOFTWARE.


Future Plans:

 - Update duplicate entries.
 - CLI, then GUI. (Front End JS?)
 - Search. (Elastic Search?)
 - Scraping the URL and getting the text back.
 - ML to pick out keywords from text and title.
 - Use that to tag and categorize the history entries
