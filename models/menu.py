response.title = settings.title
response.subtitle = settings.subtitle
response.metatitle = settings.metatitle # Custom varialbe for the head title as opposed to the h1 title
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

### Custom variables block
collections = db((db.geo_collection.id > 0) & (db.geo_collection.f_visible == True)).select(orderby=db.geo_collection.f_name)
coll_list = []
submenu = []

### Permission boolean initialization
admin = auth.has_membership('admin')
collection_admin = auth.has_membership('collection_admin')
comment_moderator = auth.has_membership('comment_moderator')

### Building main scaffolding
response.menu = [
    (T('Home'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Collections'),URL(),URL(),coll_list)
    ]
if admin or collection_admin or comment_moderator: 
    response.menu += [(T('Manage'),URL(),URL(),submenu)]

### Populating the collection list
for coll in collections: 
    coll_list += [
        (T(coll.f_name),URL('default','collection_details',vars=dict(collectionId=coll.id))==URL(),URL('default','collection_details',vars=dict(collectionId=coll.id)),[])
    ]

### Populating the Management submenu
# TODO: Determine roles and adjust logic here to represent them
if admin: 
    submenu += [
        (T('Roles'),URL('cms','roles_manage')==URL(),URL('cms','roles_manage'),[]),
        (T('Users'),URL('cms','users_manage')==URL(),URL('cms','users_manage'),[]),
        (T('Exhibits'),URL('cms','exhibits_manage')==URL(),URL('cms','exhibits_manage'),[]),
        (T('Collection'),URL('cms','display_manage')==URL(),URL('cms','display_manage'),[])
    ]
if collection_admin or admin:
    submenu += [
        (T('Items'),URL('cms','items_manage')==URL(),URL('cms','items_manage'),[])
    ]
if comment_moderator or collection_admin or admin: 
    submenu += [
        (T('Comments'),URL('cms','comments_manage')==URL(),URL('cms','comments_manage'),[]),
        (T('QR Retrieval'),URL('cms','qrret')==URL(),URL('cms','qrret'),[]),
    ]
submenu.sort()