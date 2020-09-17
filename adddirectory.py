import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
from user import User
from directory import Directory
import random

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class AddDirectory(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		directory = ' '
		user = users.get_current_user()
		logout = users.create_logout_url('/')
		directory=''
		logout = logout = users.create_logout_url('/')
		if self.request.get('button') == 'Add a Directory' :
			directory_id = self.request.get('directory_id')
			user = users.get_current_user()
			template_values = {
			'directory_id' : directory_id,
			'user' : user,
			'logout' : logout
			}

			template = JINJA_ENVIRONMENT.get_template('adddirectory.html')
			self.response.write(template.render(template_values))

		if self.request.get('button') == 'Submit' :
			
			directory_id = self.request.get('directory_id')
			directory_key = ndb.Key(Directory,directory_id)
			directory = directory_key.get()
	
			directory_path = directory.directory_path
			directory_name = self.request.get('unique_directory_name')

			checking_unique_directory_name = 0;
			for each in directory.list_of_directories :
					preprocess = each.replace('u','').replace(' ','').replace('\'','')
					sub_directory_key = ndb.Key(Directory,preprocess)
					sub_directory = sub_directory_key.get()
					if sub_directory.directory_name == directory_name :
						checking_unique_directory_name = checking_unique_directory_name + 1
						break
			if checking_unique_directory_name == 0 :
				random_id = str(random.randint(000000,999999))

				random_key = ndb.Key(Directory,random_id)
				random_value = random_key.get()

				if random_value != None :
					while (random_value!=None) :
						random_id = str(random.randint(000000, 999999))

						random_key = ndb.Key(Directory, random_id)
						random_value = random_key.get()


				if random_value == None :
					new_directory = Directory(id=random_id)
					new_directory.directory_name = directory_name
					new_directory.prev_directory = directory_id
					new_path = directory_path + directory_name + '/'
					new_directory.directory_path = new_path
					new_directory.put()

			#search = Directory.query(Directory.directory_name == directory_name).fetch()
					directory.list_of_directories.append(random_id)
					directory.put()
					self.redirect('/main')




			else :
				error_message = "Please enter a unique directory name. The directory name entered exists"
				user = users.get_current_user()
				template_values = {
					'directory_id' : directory_id,
					'error_message' : error_message,
					'user' : user,
					'logout' : logout
				}

				template = JINJA_ENVIRONMENT.get_template('adddirectory.html')
				self.response.write(template.render(template_values))




