import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
from user import User
from directory import Directory


JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class Main(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		directory = ' '
		user = users.get_current_user()
		logout = users.create_logout_url('/')
		directory_key=''
		list_directories = []
		previous_directory_id = ''
		previous_directory_name = ''
		list_files = []
		SharedFiles = []
		SharedFileOwner = []
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser_key = ndb.Key(User, user.user_id())
			myuser = myuser_key.get()
			
			if myuser == None:
				welcome = 'Welcome to the application'
				myuser = User(id=user.user_id())
				myuser.email = user.email()
				myuser.put()
				id_of_root_directory = user.email()+"/"
				directory = Directory(id=id_of_root_directory)
				directory.directory_path = '/'
				directory.directory_name = '/'
				directory.put()
				
			else :
				id_of_root_directory = user.email()+"/"
				
				directory_key = ndb.Key(Directory,id_of_root_directory)
				directory = directory_key.get()
				for each in directory.list_of_directories :
					preprocess = each.replace('u','').replace(' ','').replace('\'','')
					sub_directory_key = ndb.Key(Directory,preprocess)
					sub_directory = sub_directory_key.get()
					list_directories.append(sub_directory.directory_name)

				for each in directory.list_of_files :
					list_files.append(each)


				for index,each in enumerate(directory.shared_files):
					SharedFiles.append(each)
					owner = directory.shared_file_owner[index]
					SharedFileOwner.append(owner)
		path = directory.directory_path
		template_values = {
			'id_of_root_directory' : id_of_root_directory,
			'list_directories' : list_directories,
			'user' : user,
			'logout' : logout,
			'previous_directory_id' : directory.prev_directory,
			'previous_directory_name' : previous_directory_name,
			'list_files' : list_files,
			'shared_files': SharedFiles,
			'shared_file_owner' : SharedFileOwner,
			'path' : path
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		if self.request.get('button') == '../' :
			current_directory_id = self.request.get('directory_id')
			current_directory_key = ndb.Key(Directory,current_directory_id)
			current_directory = current_directory_key.get()
			list_directories = []
			list_files = []
			for each in current_directory.list_of_directories :
				preprocess = each.replace('u','').replace(' ','').replace('\'','')
				sub_directory_key = ndb.Key(Directory,preprocess)
				sub_directory = sub_directory_key.get()
				list_directories.append(sub_directory.directory_name)

			for each in current_directory.list_of_files :
				list_files.append(each)

			SharedFiles = []
			SharedFileOwner = []
			for index, each in enumerate(current_directory.shared_files):
				SharedFiles.append(each)
				owner = current_directory.shared_file_owner[index]
				SharedFileOwner.append(owner)
			path = current_directory.directory_path
			logout = users.create_logout_url('/')
			user = users.get_current_user()
			previous_directory_name = ''
			template_values = {
				'id_of_root_directory' : current_directory_id,
				'check' : current_directory.prev_directory,
				'list_directories' : list_directories,
				'user' : user,
				'logout' : logout,
				'previous_directory_id' : current_directory.prev_directory,
				'previous_directory_name' : previous_directory_name,
				'list_files' : list_files,
				'shared_files': SharedFiles,
				'shared_file_owner': SharedFileOwner,
				'path': path
			}
			
			template = JINJA_ENVIRONMENT.get_template('main.html')
			self.response.write(template.render(template_values))


		else :
			self.response.headers['Content-Type'] = 'text/html'
			list_directories = []
			list_files = []
			directory_name = self.request.get('hidden_directory_name')
			current_directory_id = self.request.get('directory_id')
			current_directory_key = ndb.Key(Directory,current_directory_id)
			current_directory = current_directory_key.get()
			id_of_clicked_directory = ''
			for each in current_directory.list_of_directories :
				preprocess = each.replace('u','').replace(' ','').replace('\'','')
				sub_directory_key = ndb.Key(Directory,preprocess)
				sub_directory = sub_directory_key.get()
				if sub_directory.directory_name == directory_name :
					id_of_clicked_directory = preprocess
					break

			key_of_clicked_directory = ndb.Key(Directory,id_of_clicked_directory)
			clicked_directory = key_of_clicked_directory.get()

			for each in clicked_directory.list_of_directories :
				preprocess = each.replace('u','').replace(' ','').replace('\'','')
				sub_directory_key = ndb.Key(Directory,preprocess)
				sub_directory = sub_directory_key.get()
				list_directories.append(sub_directory.directory_name)

			for each in clicked_directory.list_of_files :
				list_files.append(each)

			SharedFiles = []
			SharedFileOwner = []
			for index, each in enumerate(clicked_directory.shared_files):
				SharedFiles.append(each)
				owner = clicked_directory.shared_file_owner[index]
				SharedFileOwner.append(owner)
			path = clicked_directory.directory_path
			logout = users.create_logout_url('/')
			clicked_directory_id = clicked_directory.key.id() #change the name to id
			user = users.get_current_user()
			template_values = {
				'id_of_root_directory' : clicked_directory_id,
				'check' : current_directory.prev_directory,
				'list_directories' : list_directories,
				'user' : user,
				'logout' : logout,
				'previous_directory_id' : clicked_directory.prev_directory,
				'previous_directory_name' : clicked_directory.prev_directory,
				'list_files' : list_files,
				'shared_files' : SharedFiles,
				'shared_file_owner' : SharedFileOwner,
				'path': path
			}

			template = JINJA_ENVIRONMENT.get_template('main.html')
			self.response.write(template.render(template_values))
				
		
