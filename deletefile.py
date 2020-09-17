import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from directory import Directory
from google.appengine.api import users
from uploadfilehandler import UploadFileHandler
from directory import Directory
import random
from downloadfilehandler import DownloadFileHandler
from restore import Restore
import random
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class DeleteFile(webapp2.RequestHandler):
	def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            if self.request.get('button') == 'Delete' :
                delete_file_name = self.request.get('delete_file_name')
                directory_id = self.request.get('directory_id')
                directory_key = ndb.Key(Directory,directory_id)
                directory = directory_key.get()
                index = int(self.request.get('index'))
                blob_key = directory.blobs[index]
                del directory.list_of_files[index]
                del directory.blobs[index]
                directory.put()
                random_id = str(random.randint(000000,999999))
                random_key = ndb.Key(Directory, random_id)
                random_value = random_key.get()

                if random_value != None:
                    while (random_value != None):
                        random_id = str(random.randint(000000, 999999))

                        random_key = ndb.Key(Directory, random_id)
                        random_value = random_key.get()


                if random_value == None:
                    new_file = Restore(id=random_id)
                    new_file.put()
                    new_file_key = ndb.Key(Restore,random_id)
                    file = new_file_key.get()
                    file.file_name = delete_file_name
                    file.blob_key = blob_key
                    user = users.get_current_user()
                    email = user.email()
                    file.user = email
                    file.put()

                self.redirect('/main')

            if self.request.get('button') == 'Delete Permanently':
                file_id = self.request.get('file_id')
                file_key = ndb.Key(Restore,file_id)
                file = file_key.get()
                print(file)
                blob_key = file.blob_key
                file_key.delete()
                blobstore.delete(blob_key)
                self.redirect('/main')

            if self.request.get('button') == 'Delete Shared File' :
                directory_id = self.request.get('directory_id')
                directory_key = ndb.Key(Directory,directory_id)
                directory = directory_key.get()

                delete_file_name = self.request.get('delete_file_name')
                index = int(self.request.get('index'))

                del directory.shared_files[index]
                del directory.shared_files_blobs[index]
                del directory.shared_file_owner[index]
                directory.put()
                self.redirect('/main')




                    #new_directory = Directory(id=unique_id)
                    #new_directory.directory_name = directory_name
                    #new_directory.prev_directory = directory_id
                    #new_path = directory_path + directory_name + '/'
                    #new_directory.directory_path = new_path
                    #new_directory.put()

                    # search = Directory.query(Directory.directory_name == directory_name).fetch()
                    #directory.list_of_directories.append(random_id)
                    #directory.put()
