from google.appengine.ext import ndb


class Directory(ndb.Model):
	prev_directory = ndb.StringProperty()
	directory_name = ndb.StringProperty()
	directory_path = ndb.StringProperty()
	list_of_directories = ndb.StringProperty(repeated=True)
	list_of_files = ndb.StringProperty(repeated=True)
	blobs = ndb.BlobKeyProperty(repeated=True)
	shared_files = ndb.StringProperty(repeated=True)
	shared_files_blobs = ndb.BlobKeyProperty(repeated=True)
	shared_file_owner = ndb.StringProperty(repeated=True)

	#directory_name = ndb.StringProperty()
	#file_info = ndb.StructuredProperty(File, repeated=True)
