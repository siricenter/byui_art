### we prepend t_ to tablenames and f_ to fieldnames for disambiguity
import os

db.define_table('geo_exhibit',
    Field('f_name', type='string', required=True, requires=IS_NOT_IN_DB(db, 'geo_exhibit.f_name'),
          label=T('Exhibit Name')),
    Field('f_description', type='text', required=True,
          label=T('Description')),
    Field('f_qrcode', type='upload', uploadfolder = os.path.join(request.folder,'uploads/qrcodes'),
          label=T('QR Code')),
    Field('f_tags', type='list:string',
          label=T('Tags')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.geo_exhibit.f_name.requires=IS_NOT_EMPTY()
db.geo_exhibit.f_description.requires=IS_NOT_EMPTY()
db.geo_exhibit.f_name.requires=IS_NOT_IN_DB(db, db.geo_exhibit.f_name)

########################################
db.define_table('geo_collection',
    Field('f_name', type='string', required=True, requires=IS_NOT_IN_DB(db, 'geo_collection.f_name'),
          label=T('Collection Name')),
    Field('f_exhibit_id', type='reference geo_exhibit', required=True,
          label=T('Exhibit')),
    Field('f_qrcode', type='upload', uploadfolder = os.path.join(request.folder,'uploads/qrcodes'),
          label=T('QR Code')),
    Field('f_location', type='string', required=True, requires=IS_NOT_IN_DB(db, 'geo_collection.f_location'),
          label=T('Location')),
    Field('f_tags', type='list:string',
          label=T('Tags')),
    Field('f_visible', type='boolean',
          label=T('Visible?')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.geo_collection.f_name.requires=IS_NOT_EMPTY()
db.geo_collection.f_exhibit_id.requires=IS_NOT_EMPTY()
db.geo_collection.f_location.requires=IS_NOT_EMPTY()
db.geo_collection.f_exhibit_id.requires=IS_IN_DB(db, db.geo_exhibit.id,lambda row: '%s' % row.f_name)
db.geo_collection.f_name.requires=IS_NOT_IN_DB(db, db.geo_collection.f_name)
db.geo_collection.f_location.requires=IS_NOT_IN_DB(db, db.geo_collection.f_location)

########################################
db.define_table('geo_item',
    Field('f_name', type='string', required=True, requires=IS_NOT_IN_DB(db, 'geo_item.f_name'),
          label=T('Item Name')),
    Field('f_collection_id', type='reference geo_collection', required=True,
          label=T('Collection')),
    Field('f_description', type='text',
          label=T('Description')),
    Field('f_image', type='upload',
          label=T('Image')),
    Field('f_thumb', type='upload', uploadfolder = os.path.join(request.folder,'uploads/thumbs'),
          label=T('Thumbnail')),
    Field('f_qrcode', type='upload', uploadfolder = os.path.join(request.folder,'uploads/qrcodes'),
          label=T('QR Code')),
    Field('f_tagline', type='string', # Loads to subtitile (ie. Scientific name)
          label=T('Tag Line')),
    Field('f_featured', type='boolean', default=False,
          label=T('Featured')),
    Field('f_alt1', type='string', # Artist
          label=T('Artist')),
    Field('f_alt2', type='string', # Location
          label=T('Location')),
    Field('f_alt3', type='string', # Composition
          label=T('Composition')),
    Field('f_alt4', type='string', # Dimensions
          label=T('Dimensions')),
    Field('f_alt5', type='string', # Sample Number
          label=T('Sample Number')),
    Field('f_alt6', type='string', # Donor
          label=T('Donor')),
    Field('f_alt7', type='string', # Time Period
          label=T('Time Period')),
    Field('f_youtube1', type='string',
          label=T('YouTube Video 1')),
    Field('f_youtube2', type='string',
          label=T('YouTube Video 2')),
    Field('f_wiki', type='string', # Wikipedia Article
          label=T('Wikipedia Article')),
    Field('f_link', type='string', # Other External Site
          label=T('External Website')),
    Field('f_image2', type='upload', # Additional Images
          label=T('Image 2')),
    Field('f_image3', type='upload', # Additional Images
          label=T('Image 3')),
    Field('f_extImg1', type='string', # Additional Images from web
          label=T('External Image 1')),
    Field('f_extImg2', type='string', # Additional Images from web
          label=T('External Image 2')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.geo_item.f_name.requires=IS_NOT_EMPTY()
db.geo_item.f_name.requires=IS_NOT_IN_DB(db, db.geo_item.f_name)
db.geo_item.f_collection_id.requires=IS_NOT_EMPTY()
db.geo_item.f_collection_id.requires=IS_IN_DB(db, db.geo_collection,lambda row: '%s' % row.f_name)
db.geo_item.f_featured.default=False
db.geo_item.f_image.requires=IS_EMPTY_OR(IS_IMAGE())
db.geo_item.f_extImg1.requires=IS_EMPTY_OR(IS_URL())
db.geo_item.f_extImg2.requires=IS_EMPTY_OR(IS_URL())
########################################
db.define_table('t_tour',
    Field('f_name', type='string', required=True, requires=IS_NOT_IN_DB(db, 't_tour.f_name'),
          label=T('Tour Name')),
    Field('f_description', type='text',
          label=T('Description')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

db.t_tour.f_name.requires=IS_NOT_EMPTY()
db.t_tour.f_name.requires=IS_NOT_IN_DB(db, db.t_tour.f_name)

########################################
db.define_table('t_item_comment',
    Field('f_comment', type='text', required=True,
          label=T('Comment Text')),
    Field('f_item_id', type='reference geo_item', required=True,
          label=T('Item')),
    Field('f_status', type='string', required=True, default='Pending',
          label=T('Status')),
    auth.signature,
    migrate=settings.migrate)

db.t_item_comment.f_comment.requires=IS_NOT_EMPTY()
db.t_item_comment.f_status.requires=IS_IN_SET(('Pending','Approved','Rejected'))
db.t_item_comment.f_status.default='Pending'

########################################
db.define_table('t_coll_comment',
    Field('f_comment', type='text', required=True,
          label=T('Comment Text')),
    Field('f_collection_id', type='reference geo_collection', required=True,
          label=T('Collection')),
    Field('f_status', type='string', required=True, default='Pending',
          label=T('Status')),
    auth.signature,
    migrate=settings.migrate)

db.t_coll_comment.f_comment.requires=IS_NOT_EMPTY()
db.t_coll_comment.f_status.requires=IS_IN_SET(('Pending','Approved','Rejected'))
db.t_coll_comment.f_status.default='Pending'
