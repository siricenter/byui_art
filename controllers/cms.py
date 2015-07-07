# coding: utf8
# TODO: Determine group architecture and edit the  @auth.requires fields as needed

# Membership booleans:
admin = auth.has_membership('admin')
collection_admin = auth.has_membership('collection_admin')
comment_moderator = auth.has_membership('comment_moderator')

@auth.requires(admin)
def exhibits_manage():
    response.metatitle += " - Exhibit Management"
    response.title = "Exhibit"
    response.subtitle = "Management"
    db.geo_exhibit.f_qrcode.writable = False
    form = SQLFORM.smartgrid(db.geo_exhibit,links_in_grid=False,
        oncreate=exhi_create)
    return dict(form=form)

@auth.requires(collection_admin or admin)
def display_manage():
    response.metatitle += " - Collection Management"
    response.title = "Collection"
    response.subtitle = "Management"
    db.geo_collection.f_qrcode.writable = False
    form = SQLFORM.smartgrid(db.geo_collection,links_in_grid=False,
        oncreate=coll_create)
    return dict(form=form)

@auth.requires(collection_admin or admin)
def items_manage():
    response.metatitle += " - Item Management"
    response.title = "Item"
    response.subtitle = "Management"
    db.geo_item.f_qrcode.writable = False
    db.geo_item.f_thumb.writable = False
    form = SQLFORM.smartgrid(db.geo_item,links_in_grid=False,oncreate=item_create,onupdate=item_create,
        fields=(
            db.geo_item.id,
            db.geo_item.f_name,
            db.geo_item.f_collection_id,
            db.geo_item.f_description,
            db.geo_item.f_tagline,
            db.geo_item.f_featured,
            db.geo_item.is_active,
            db.geo_item.f_qrcode))
    return dict(form=form)

@auth.requires(comment_moderator or collection_admin or admin)
def comments_manage():
    subset = request.vars['show']
    response.metatitle += " - Comment Moderation"
    response.title = "Comment"
    response.subtitle = "Moderation"
    # All logic is built into the modules, within the comments.py controller
    return dict(subset=subset)

@auth.requires(collection_admin or admin)
def tours_manage():
    form = SQLFORM.smartgrid(db.t_tour,links_in_grid=False)
    return dict(form=form)

@auth.requires(admin)
def users_manage():
    response.metatitle += " - User Management"
    response.title = "User"
    response.subtitle = "Management"
    form = SQLFORM.smartgrid(db.auth_user,links_in_grid=False,
        fields=(db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email))
    return dict(form=form)

@auth.requires(admin)
def roles_manage():
    response.metatitle += " - Role Management"
    response.title = "Role"
    response.subtitle = "Management"
    form = SQLFORM.smartgrid(db.auth_membership,links_in_grid=False,
        fields=(db.auth_membership.user_id,db.auth_membership.group_id))
    return dict(form=form)

def qrret():
    response.metatitle += " - QR Code Printing"
    response.title = "QR Code"
    response.subtitle = "Printing"
    rows = db().select(db.geo_item.f_name,db.geo_item.f_qrcode, orderby=db.geo_item.f_name)
    rows2 = db().select(db.geo_collection.f_name, db.geo_collection.f_qrcode, orderby=db.geo_collection.f_name)
    items=[]
    colls=[]
    sizes = [
        OPTION("All labels with have equal width and height", _disabled=True),
        OPTION("0.5 inch", _value=0.5),OPTION("0.75 inch", _value=0.75),
        OPTION("1 inch", _value=1.0),OPTION("1.5 inch", _value=1.5, _selected=True),
        OPTION("2 inch", _value=2.0),OPTION("2.5 inch", _value=2.5),
        OPTION("3 inch", _value=3.0),OPTION("3.5 inch", _value=3.5),
        OPTION("4 inch", _value=4.0),OPTION("4.5 inch", _value=4.5),
        OPTION("5 inch", _value=5.0)
    ]
    for row in rows:
        items += [
        OPTION(row.f_name, _value=row.f_qrcode)
        ]
    for row in rows2:
        colls += [
        OPTION(row.f_name, _value=row.f_qrcode)
        ]
    fields = [DIV(H4("Size per code:"), SELECT(sizes, _name="retsizes"), _class="span12"),
        DIV(H4("Items"), SELECT(items, _name="retitems", _multiple=True, _size=10), _class="span6"),
        DIV(H4("Collections"), SELECT(colls, _name="retcolls", _multiple=True, _size=10), _class="span6"), BR(),
        DIV(INPUT(_type='submit', _value="Get QR Codes"), _style="margin-top: 20px", _class="span12")]
    form=FORM(fields)
    if form.process(onvalidation=qrparse).accepted:
        response.flash = 'Generated pages below'
    return dict(form=form)

##################################
##### Onvalidation functions #####
##################################

# Imports for all functions are here
import os
import uuid
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import qrcode

# Oncreate function from the item_manage view
def item_create(form):
    record = db(db.geo_item.f_name == request.vars.f_name).select().first()
    if record.f_qrcode == None:
        arg = str(record.id)
        path = 'http://siri.pythonanywhere.com/byui_art/default/item_details?itemId=' + arg + '&qr=True'
        code = qrcode.make(path)
        qrName='geo_item.f_qrcode.%s.jpg' % (uuid.uuid4())
        code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
        record.update_record(f_qrcode=qrName)
    if record.f_image != form.vars.f_image:
        try:
            image = Image.open(request.folder + 'uploads/' + form.vars.f_image)
            image.thumbnail((150, 150), Image.ANTIALIAS)
            imgName='geo_item.f_thumb.%s.jpg' % (uuid.uuid4())
            image.save(request.folder + 'uploads/thumbs/' + imgName, 'JPEG')
            record.update_record(f_thumb=imgName)
        except:
            pass
    return dict()

# Oncreate function from the collection_manage view
def coll_create(form):
    record = db(db.geo_collection.f_name == request.vars.f_name).select().first()
    arg = str(record.id)
    path = 'http://siri.pythonanywhere.com/byui_art/default/collection_details?collectionId=' + arg + '&qr=True'
    code = qrcode.make(path)
    qrName='geo_collection.f_qrcode.%s.jpg' % (uuid.uuid4())
    code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    record.update_record(f_qrcode=qrName)
    return dict()

# Oncreate function from the exhibit_manage view
def exhi_create(form):
    record = db(db.geo_exhibit.f_name == request.vars.f_name).select().first()
    arg = str(record.id)
    path = 'http://siri.pythonanywhere.com/byui_art/default/exhibit_details?exhibitId=' + arg + '&qr=True'
    code = qrcode.make(path)
    qrName='geo_exhibit.f_qrcode.%s.jpg' % (uuid.uuid4())
    code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    record.update_record(f_qrcode=qrName)

# Onvalidation function for the qrret* view
def qrparse(form):
    codes = []
    codes += form.vars.retitems
    codes += form.vars.retcolls
    size = form.vars.retsizes
    session.qr = qrmake(codes, size)


# This function accepts an array of filenames and programatically opens the images and pastes them
# onto blank images. The images are returned as an array
def qrmake(codes, size_in):
    images = []
    dpi = 150 # Dots Per Inch
    background = Image.new('RGBA', (int(8.5 * dpi), int(11 * dpi)), (255, 255, 255, 255))
    margin = dpi
    bg_w,bg_h=background.size
    offset_left = margin
    offset_down = margin
    rowend = bg_w - margin
    pageend = bg_h - margin
    size = int(float(size_in) * dpi)
    dimen = (size,size)
    for i in xrange(len(codes)):
        code = codes[i]

        # Tries to open the image and continues to the next iteration if it fails
        try:
            img = Image.open(request.folder + 'uploads/' + code)
        except:
            continue
        img_w,img_h=img.size
        if img_w > size:
            img.thumbnail(dimen, Image.ANTIALIAS)
        else:
            img = img.resize(dimen)
        img_w,img_h=img.size

        pasted = False
        while pasted == False:

            # Check to see if the image will be too wide to fit on the page
            if offset_left + img_w > rowend:
                offset_down += img_h
                offset_left = margin

            # Check to see if the page has ended and if so, recursively calls the function then returns
            elif offset_down + img_h > pageend:
                qrName='qrpage.%s.jpeg' % (uuid.uuid4())
                background.save(request.folder + 'static/temp/' + qrName, 'JPEG')
                images += [qrName]
                images += qrmake(codes[i:],size_in)
                return images

            # When the image fits, it is pasted here
            else:
                background.paste(img,(offset_left,offset_down))
                offset_left += img_w
                pasted = True

    # Adds the single image to the array and returns when no recursion occured
    qrName="qrpage.%s.jpeg" % (uuid.uuid4())
    background.save(request.folder + 'static/temp/' + qrName, 'JPEG')
    images += [qrName]
    return images

# fix qr codes that were going to the wrong place
@auth.requires(admin)
def fix_qr():
    response.metatitle += " - Fix QR Codes"
    response.title = "Admin"
    response.subtitle = "Stuff"
    exhibits = db(db.geo_exhibit).select()
    collections = db(db.geo_collection).select()
    items = db(db.geo_item).select()

    item = db(db.geo_item).select().first()
    arg = str(item.id)
    path = 'http://siri.pythonanywhere.com/byui_art/default/item_details?itemId=' + arg + '&qr=True'
    code = qrcode.make(path)
    qrName = 'geo_item.f_qrcode.%s.jpg' % (uuid.uuid4())
    folder = request.folder
    code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    qr_text(qrName, item.f_name, item.f_alt5)
    item.update_record(f_qrcode=qrName)

    # for exhibit in exhibits:
    #     arg = str(exhibit.id)
    #     path = 'http://siri.pythonanywhere.com/byui_art/default/exhibit_details?exhibitId=' + arg + '&qr=True'
    #     code = qrcode.make(path)
    #     qrName = 'geo_exhibit.f_qrcode.%s.jpg' % (uuid.uuid4())
    #     folder = request.folder
    #     code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    #     exhibit.update_record(f_qrcode=qrName)

    # for collection in collections:
    #     arg = str(collection.id)
    #     path = 'http://siri.pythonanywhere.com/byui_art/default/collection_details?collectionId=' + arg + '&qr=True'
    #     code = qrcode.make(path)
    #     qrName = 'geo_collection.f_qrcode.%s.jpg' % (uuid.uuid4())
    #     folder = request.folder
    #     code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    #     collection.update_record(f_qrcode=qrName)

    # for item in items:
    #     arg = str(item.id)
    #     path = 'http://siri.pythonanywhere.com/byui_art/default/item_details?itemId=' + arg + '&qr=True'
    #     code = qrcode.make(path)
    #     qrName = 'geo_item.f_qrcode.%s.jpg' % (uuid.uuid4())
    #     folder = request.folder
    #     code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    #     item.update_record(f_qrcode=qrName)

    #record = db(db.geo_collection.f_name == request.vars.f_name).select().first()
    #arg = str(record.id)
    #path = 'http://siri.pythonanywhere.com/byui_art/default/collection_details?collectionId=' + arg + '&qr=True'
    #code = qrcode.make(path)
    #qrName='geo_collection.f_qrcode.%s.jpg' % (uuid.uuid4())
    #code.save(request.folder + 'uploads/qrcodes/' + qrName, 'JPEG')
    #record.update_record(f_qrcode=qrName)
    return locals()

# add text to the qr code to identify where it should go
@auth.requires(admin)
def qr_text(filename, topTxt, bottomTxt):
    path = os.path.join(request.folder,'uploads/qrcodes',filename)
    img = Image.open(path)
    # get the width and height for adjustment
    (width, height) = img.size
    adjHeight = height-25
    # adding in the text
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',20)
    draw.text((10, 10),topTxt,100,font=font)
    draw.text((10, adjHeight),bottomTxt,100,font=font)
    # re-save
    img.save(request.folder + 'uploads/qrcodes/' + filename, 'JPEG')

    # # original test code
    # tst = db(db.geo_item).select().first()
    # tsttarget = 'evancaldwell.com'
    # tstqrName = 'toEvan.jpg'
    # tstcode = qrcode.make(tsttarget)
    # # saving
    # tstcode.save(request.folder + 'uploads/tst/' + tstqrName, 'JPEG')
    # # reopen image to add text
    # folder = request.folder
    # midpath = 'byui_art/default/download/tst/'
    # fullpath = os.path.join(request.folder,'uploads/tst',tstqrName)
    # tstimg = Image.open(fullpath)
    # # get the width and height for adjustment
    # (width, height) = tstimg.size
    # adjHeight = height-25
    # # adding in the text
    # draw = ImageDraw.Draw(tstimg)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',15)
    # draw.text((2, 2),"Evan Caldwell",100,font=font)
    # draw.text((2, adjHeight),"evancaldwell.com",100,font=font)
    # # re-save
    # tstimg.save(request.folder + 'uploads/tst/' + tstqrName, 'JPEG')



