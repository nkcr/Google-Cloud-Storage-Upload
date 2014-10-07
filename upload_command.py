# -*- coding: utf-8 -*- 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Message describing how to use the script.
USAGE = """
Uploads the result of a command to storage
Note : Uploaded as text/plain format

Usage examples:
  $ python upload_command.py "ls -la" gs://bucket/object
  $ python
"""

# You need to create a service account key
# see here http://bit.ly/1tprtJc
# Also provide the email associated with the key
# Path is relative
PRIVATTE_KEY_PATH = 'Backups-6b883fdec558.p12'
EMAIL_KEY = '1067891787564-ms8k3bb85eet1aueb372p6t95dri83ss@developer.gserviceaccount.com'

import httplib2 # handle http stuff
import os # handle file
import sys # handle commmand line args 
import io # for plain text upload (nkcr)
import json # to display the result (nkcr)
import subprocess # to make pg_dump or whatever unix command
from apiclient.discovery import build as discovery_build
from oauth2client.client import SignedJwtAssertionCredentials
# for key auth (nkcr)
from apiclient.http import MediaIoBaseUpload

RW_SCOPE = 'https://www.googleapis.com/auth/devstorage.read_write'

def get_authenticated_service(scope):
  print 'Authenticating...' 

  f = file(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   PRIVATTE_KEY_PATH)), 'rb')
  key = f.read()
  f.close()

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with the Credentials. Note that the first parameter, service_account_name,
  # is the Email address created for the Service account. It must be the email
  # address associated with the key that was created.
  credentials = SignedJwtAssertionCredentials(
      EMAIL_KEY,
      key,
      scope=scope)
  http = httplib2.Http()
  http = credentials.authorize(http)

  return discovery_build('storage', 'v1', http=http)


def upload(argv):

  command = argv[1]
  bucket_name, object_name = argv[2][5:].split('/', 1)
  assert bucket_name and object_name

  service = get_authenticated_service(RW_SCOPE)

  content = subprocess.check_output(command,shell = True)

  print 'Building upload request...'
  #media = MediaFileUpload(filename, chunksize=CHUNKSIZE, resumable=True)
  media = MediaIoBaseUpload(io.BytesIO(content), 'text/plain;charset=utf-8')
  request = service.objects().insert(bucket=bucket_name, name=object_name,
                                     media_body=media)

  print 'Uploading file: %s to bucket: %s object: %s ' % (command, bucket_name,
                                                          object_name)
  resp = request.execute()
  print json.dumps(resp, indent=2)

  print '\nUpload complete!'

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print 'Too few arguments.'
    print USAGE
  if sys.argv[2].startswith('gs://'):
    upload(sys.argv)
  else:
    print USAGE