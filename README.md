# LibraryDatabase
A Command line simulation of a simple Library Database System using SQLite.

This is a command line app which simulates a library database. The users can use this to find items like CDs or books that are currently in stock or find information about the availability of items. The user can then borrow the item which will mark that item as unavailable. The application also allows the user to reserve a event room and register for events. Information like the availability of items, who has borrowed which item and what rooms have been booked are stored in a SQLite database. This database is queried for the app features like checking the users currently borrowed items and returning items to the library.

## Running the Application
Run `AppUI.py` using `python AppUI.py`to start the program, in [Anaconda](https://www.anaconda.com/) for ease of use.

The minimum requirement is Python 3.10 but I recommend downloading the latest version from [here](https://www.python.org/downloads/)
