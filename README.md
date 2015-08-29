# uw-publisher

This flask server receives communication from the [uw-web](https://github.com/unfoldingWord-dev/uw-web) client
and exports the chosen Bible text into any format the user desires.

# Developer Setup

To use this tool, you will first need to make sure you have [Python 3](https://docs.python.org/3/using/) installed.  Once installed, you can follow these steps to get started:

1) Install [Flask](http://flask.pocoo.org) using PIP3.

    sudo pip3 install flask

2) Create 2 directories to store temporary files and source files.
3) Copy a version of the 'sample.config.json' file to 'config.json'.

    cp sample.config.json config.json

4) Open the config file, and set all the appropriate settings.

    * port - The port to run the Flask Server on.
    * source_root - The location of the directory you created that will store source files.
    * temp_root - The location of the directory you created that will store temporary files.

5) Run the flask server.

    python3 ./server.py
