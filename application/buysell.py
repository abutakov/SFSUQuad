#!/usr/bin/env python3

################################
#         buysell.py           #
# Main application module      #
# (run this)                   #
# Created by:                  #
# Emanuel Saunders(Nov 22,2019)#
################################

from app import app, db
from app.models import User, Post, Message, Category

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User, 'Post':Post,'Message':Message,'Category':Category}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)