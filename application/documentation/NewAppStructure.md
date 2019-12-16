# NEW FLASK MVC app structure

## AS of Decemeber 1, 2019

### By Emanuel Saunders

As of the 1st of december the app is following a new more organized and modular structure to make compenents easier to manage.

The main app is run via `buysell.py` in the outermost directory of the application folder.

config

All routing logic is done via the routes file.


### For unit testing the Flask Shell can be used, to set up the shell properly use: 
    `export FLASK_APP=buysell.py`


## Flask Login: 
 four required items for login:


is_authenticated: a property that is True if the user has valid credentials or False otherwise.
is_active: a property that is True if the user's account is active or False otherwise.
is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python 2).