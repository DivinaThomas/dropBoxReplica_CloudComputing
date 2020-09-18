from google.appengine.ext import ndb
from directory import Directory

class User(ndb.Model):
	email = ndb.StringProperty()
	
	#directory_info = ndb.StructuredProperty(Directory, repeated=True)
	
