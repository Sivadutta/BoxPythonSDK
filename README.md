# BoxPythonSDK
Script to create folder in Box and add collaboration to it.
Request Box API for newly created users on a given date.
Search for active users in Box.
Search for particular named folder in Box, if exist: don't create the same named folder; else create.
Create folder as a particular user(not as APP user).
Add colloborators in the newly created folder.

Requirement: 1. Box API with enterprise settings.
2. API config file.
3. Third party free libraries: boxsdk, iso8601, pytz.


Complete steps for development & distributre:

1. Create virtual environment. It will help to encapsulate all the python libraries into one folder. Please follow the link: https://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
2. Include dependent libraries list:asn1crypto==0.24.0
attrs==19.1.0
boxsdk==2.5.0
certifi==2019.3.9
cffi==1.12.2
chardet==3.0.4
cryptography==2.6.1
idna==2.8
pycparser==2.19
PyJWT==1.7.1
requests==2.21.0
requests-toolbelt==0.9.1
six==1.12.0
urllib3==1.24.1
wrapt==1.11.1
3. For making exe: install pyinstaller.
4. Pyinstaller won't recognise all the libraries of Boxsdk. So, make spec file which will be used by the pyinstaller to make exe. Explained here: https://pythonhosted.org/PyInstaller/spec-files.html
5.Include all box libraries inside hiddenimports=[]. Like:  hiddenimports=[
'boxsdk.object.collaboration',
'boxsdk.object.collaboration_whitelist',
'boxsdk.object.web_link'],
6. If he Box API generated config.json file used in python code as: open file, read... it might not work. Copy, paste the clientid, clientsecret etc. to a .py file. Then it will work, tested/deployed in production environment.
7. Create python exe by using spec file: pyinstaller --onefile <your spec file name>
8. Distribute the exe & enjoy.



