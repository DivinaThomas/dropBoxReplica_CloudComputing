from google.appengine.ext import ndb


class Restore(ndb.Model):
    user = ndb.StringProperty()
    file_name = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
