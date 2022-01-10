from __future__ import print_function
import os

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

FOLDER_MIME = 'application/vnd.google-apps.folder'
    
def auth_drive():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_2.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds
    

def list_res(DRIVE):
    files = DRIVE.files().list().execute().get('files')
    # for f in files:
    #     print(f['name'], f['mimeType'], f['id'])
    return files

def create_folder(DRIVE, list_res, folder = 'Temp'):
    for f in list_res:
        if folder == f['name'] and f['mimeType'] == FOLDER_MIME:
            print("Папка существует") 
            return f['id']
        else:     
            body = {'name': folder, 'mimeType': FOLDER_MIME}
            return DRIVE.files().create(body=body, fields='id').execute().get('id')


def load_file(DRIVE, folder_googledisk_id = None, mimetype = None, filename = "5.jpg", folder = "temp"):
    '''folder_googledisk_id - идентификатор папки на гугл диске'''
    metadata = {'name': filename, 'parents': [folder_googledisk_id]} if folder_googledisk_id != None else {'name': filename}
    if mimetype:
        metadata['mimeType'] = mimetype
    media_body = os.getcwd() + os.sep + folder + os.sep + filename
    res = DRIVE.files().create(body=metadata, media_body = media_body).execute()
    if res:
        print('Uploaded "%s" (%s)' % (filename, res['mimeType']))





if __name__ == '__main__':
    DRIVE = discovery.build('drive', 'v3', http=auth_drive().authorize(Http()))
    list_res = list_res()
    print(list_res)
    # load_file()