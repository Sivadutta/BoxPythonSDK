# developed in Python 3.7.3 - see requirements.txt for other dependencies
from boxsdk import JWTAuth, Client
from utils import *
import json
from boxsdk.exception import BoxAPIException

configFileName = ''
#if pyinstaller unable to deal with json file, then copy,paste values from json file to below.
with open(configFileName, 'r') as data_file:
    ''' Import the Config file and create a keyfile '''
    data = json.load(data_file)

    enterprise_id = data['enterpriseID']
    client_id = data['boxAppSettings']['clientID']
    client_secret = data['boxAppSettings']['clientSecret']
    rsakey_passphrase = str(data['boxAppSettings']['appAuth']['passphrase'])
    jwt_key_id = data['boxAppSettings']['appAuth']['publicKeyID']

    # This will create the key file from the config file
    keyfilename = "private_key.crt"
    with open(keyfilename, 'w') as kfile:
        kfile.write(str(data['boxAppSettings']['appAuth']['privateKey']))
    rsakey_filename = keyfilename

try:
    auth = JWTAuth(
        client_id=client_id,
        client_secret=client_secret,
        enterprise_id=enterprise_id,
        jwt_key_id=jwt_key_id,
        rsa_private_key_file_sys_path=rsakey_filename,
        rsa_private_key_passphrase=rsakey_passphrase,
        # network_layer=
    )
except BoxAPIException as e:
    pr('failed to get auth' + str(e))

try:
    access_token = auth.authenticate_instance()
    ''' Tell the SDK to make the call to get a live token '''
except BoxAPIException as e:
    pr('failed to autheticate instance' + str(e))

try:
    sa_client = Client(auth)
    ''' Initialize a Client wrapper 'client' '''
except BoxAPIException as e:
    pr('failed to Initialize a client wrapper' + str(e))

#me = sa_client.user().get()
#pr('You are logged in as user: ' + me.name, me.id, me.status)
