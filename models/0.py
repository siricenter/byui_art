from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.metatitle = 'Geology Musuem'
settings.title = 'QR Platform'
settings.subtitle = 'Rich content, ease of use, quality of work'
settings.author = 'Evan Caldwell'
settings.author_email = 'e.caldwell@sirinstitute.org'
settings.keywords = 'qr, museum, gallery, university'
settings.description = 'This is a platform to allow access to rich content for museums, galleries and universities via a simple QR code setup.'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'fd06c333-4922-400d-886b-d119a2c6d1be'
settings.email_server = 'localhost'
settings.email_sender = 'info@sirinstitute.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
