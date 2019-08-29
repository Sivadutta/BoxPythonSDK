from boxsdk.object.collaboration import CollaborationRole
from boxsdk.exception import BoxAPIException
from auth import sa_client
from boxsdk.object.events import Events
from datetime import datetime
import iso8601
import pytz
from boxsdk.object.collaboration import CollaborationRole

'''Test root folder ID '''
Root_Folder_Id = ''

def GetBoxNewUserEvent():
	''' Get new Box User information from events occured for a particular day'''
	subfolderId = 0
	events = sa_client.events().get_admin_events(created_after='2019-08-26T09:12:36-00:00',
		event_types=['NEW_USER'])
	events = events['entries']
	if not events:
		return
	for k in events:
		dtime = get_date_string(k['created_at'])
		dtime = dtime.date()
		today = datetime.now().date()#Get the last run time from schedular/log file latest time & run after that time.		
		if(dtime == today):
				if k['event_type'] == 'NEW_USER':
					if(not chkExistUserFolder(k['source']['login'])):
						createSharedFolder(k['source']['login'])


	return subfolderId

def get_date_string(objDate):
	dt = iso8601.parse_date(objDate)
	dt = dt.astimezone(pytz.utc)
	dt=datetime.strptime(str(datetime.strftime(dt,'%Y-%m-%d %H:%M:%S')),'%Y-%m-%d %H:%M:%S')	
	return dt

def chkExistUserFolder(userEmail):
	''' get Box User information from email supplied '''
	existedFolder = True
	try:
		boxUsers = sa_client.users(limit=1000, offset=0, filter_term=userEmail)
		for boxUser in boxUsers:
			boxUserId = boxUser.id

			if boxUserId and boxUser.status == 'active':
				existedFolder = search_folder(sa_client, boxUser.login)
			else:
				existedFolder = False
				pr('- User account may not exist or has been marked as inactive')
	except(BoxAPIException, e):
		pr('- Exiting Script!! - Please check user has a Box account'+ e)


	return existedFolder

def search_folder(client, userEmail):
	isFolder = True
	try:
		share_folderName = "-Shared Folder ("+userEmail+")"
		search_results = client.search().query(share_folderName, limit=2, offset=0)
		for item in search_results:
			isFolder = True
			item_with_name = item.get(fields=['name'])
			print('matching item: ' + item_with_name.id)
		else:
			isFolder = False
			print('no matching items'+share_folderName + "userEmail:"+userEmail)

	except(BoxAPIException, e):
		pr('- Exiting Script!! - User has a shared Box folder'+ e)

	
	return isFolder	

def createSharedFolder(userEmail):
	subfolderId = 0;
	try:
		serviceAc = impersonateAccount()
		main_folder = sa_client.as_user(serviceAc).folder(folder_id=Root_Folder_Id).get()
		subfolder = main_folder.create_subfolder('-Shared Folder ('+userEmail+')')
		subfolderId = subfolder.get()['id']
		collaboration = subfolder.add_collaborator(userEmail, CollaborationRole.CO_OWNER)
		print('Created a collaboration on folder'+ subfolder.get()['id'])
		
	except(BoxAPIException, e):
		pr('- Exiting Script!! - User has a shared Box folder'+ e)

	return subfolderId

def impersonateAccount():
	userId = "";	
	serviceAC = sa_client.user(user_id=userId).get()	

	return serviceAC

def main():
	GetBoxNewUserEvent()


if __name__ == '__main__':
	main()
