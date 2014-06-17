Google-Cloud-Storage-Upload
===========================

Script to upload the result of a command to google cloud storage. Greater for dump backup.
<p align="center"><img src="http://s27.postimg.org/p8rtjh2db/Untitled_1.png"></p>

Purpose
--------

This script is for Google cloud storage, it uses Google python client library to send the result of a command to a bucket (for example save the result of a pg_dump or whatever you want). Don't need to provide password each time, it is made to be used fully alone.<br>
Note : it saves files with *text/plain;charset=utf-8*


Prerequisite
--------
The google-api-python library must be installed. See https://github.com/google/google-api-python-client


Setup
--------
If not already done, create a project in your console developer (https://console.developers.google.com) and create a new bucket in the cloud storage area (you may before need to activate google cloud storage api).<br>
You need to edit the script with your key path and your email key (see security section). <br>

Security
--------
To access your bucket, you must provide a service account key and an email. To do so, look at your *api & auth* section of your console developer (see http://bit.ly/1tprtJc). After that, provide the given file to the script by setting PRIVATE_KEY_PATH.

RUN
--------
You must provide to the script your command and your bucket. Examples : <br>
$ python upload_command.py "ls -la" gs://bucket/object <br>
$ python upload_command.py "pg_dump my_database" gs://bucket/object

Encrypt content
--------
Sometimes you'll want to encrypt your data before storing. It might be a good thing. <br>
Nothing more easy. You can pipe your command with something that encrypt your data. For example with aescript (see http://www.aescrypt.com/) you can do that : <br>
$ python upload_command.py "pg_dump my_database | aescrypt -e -k storage.key - "gs://my-bucket-ch/pgsql/$(date +\%Y-\%m-\%d-\%H\%M).sql.aes

