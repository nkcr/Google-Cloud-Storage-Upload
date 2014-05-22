Google-Cloud-Storage-Upload
===========================

Script to upload the result of a command to google cloud storage. Used for dump backup.


Purpose
--------

This script is for google cloud storage, it use google python client library to send the result of a command to a bucket (for example save the result of a pg_dump or whatever you want). Don't need to provide password each time, it is made to be used fully alone.


Prerequiste
--------
The google-api-python library must be installed. See https://github.com/google/google-api-python-client


Setup
--------
If not already done, create a project in your console developer (https://console.developers.google.com) and create a new bucket in the cloud storage area (you may before need to activate google cloud storage api).<br>
You need to edit the script with your key path and your email key (see security section). <br>

Security
--------
To access your bucket, you must provide a service account key and an email. To do so, look at your *api & auth* section of your console developer (see http://bit.ly/1tprtJc).

RUN
--------
Call the script like that : <br>
$ python upload_command.py "ls -la" gs://bucket/object <br>
$ python upload_command.py "pg_dump my_database" gs://bucket/object



