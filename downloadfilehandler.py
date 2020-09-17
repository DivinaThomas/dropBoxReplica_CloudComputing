import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from directory import Directory
class DownloadFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Download Shared File':
			index = int(self.request.get('index'))
			directory_id = self.request.get('directory_id')
			directory_key = ndb.Key(Directory, directory_id)
			directory = directory_key.get()
			file_name = self.request.get('file_name')
			self.send_blob(directory.shared_files_blobs[index])

		if self.request.get('button') == 'Download':
			index = int(self.request.get('index'))
			directory_id = self.request.get('directory_id')
			directory_key = ndb.Key(Directory, directory_id)
			directory = directory_key.get()
			file_name = self.request.get('file_name')
			directory.put()
			self.send_blob(directory.blobs[index])


