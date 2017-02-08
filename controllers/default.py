import os
import uuid
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import qrcode

# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def index():
    response.title = "Welcome to the QR Platform"
#     response.subtitle = "Take a few minutes to explore, learn and discover."
    response.subtitle = "Performing Maintenance."
    exhibits = db(db.geo_exhibit).select()
    return dict(exhibits=exhibits)

def error():
    return dict()

def exhibit_details():
#     redirect(URL('index'))
    exhibitId = request.vars['exhibitId']
    userAgent = request.user_agent()
    if (userAgent.is_mobile == True):
        colls = 1
    else:
        colls = 3
    try:
        exhibit = db(db.geo_exhibit.id == exhibitId).select().first()
        response.metatitle += " - " + exhibit.f_name
        response.title = exhibit.f_name
        response.subtitle = exhibit.f_description
        collections = db((db.geo_collection.f_exhibit_id == exhibitId) & (db.geo_collection.f_visible == True)).select()
        exhibit_items = db(db.geo_item.f_collection_id.belongs(collections)).select()
        height = find_max_height_collection(collections, colls, exhibit_items)
        #featuredItems = db((db.geo_item.f_featured == 1) & (db.geo_item.id.belongs(exhibit_items))).select()
    except:
        response.title = 'Navigation Error'
        response.subtitle = 'Invalid exhibit'
        response.flash = 'Please use navigation from index to select an exhibit'
    
    return locals()

def collection_details():
#     redirect(URL('index'))
    collectionId = request.vars['collectionId']
    userAgent = request.user_agent()
    if (userAgent.is_mobile == True):
        colls = 1
    else:
        colls = 3
    try:
        collection = db(db.geo_collection.id == collectionId).select().first()
        response.metatitle += " - " + collection.f_name
        response.title = collection.f_name
        response.subtitle = collection.f_location
        featuredItems = db((db.geo_item.f_collection_id == collectionId) & (db.geo_item.f_featured == 1)).select()
        items = db(db.geo_item.f_collection_id == collectionId).select()
        height = find_max_height(items, colls)
        comments=db((db.t_coll_comment.f_collection_id == collectionId) & (db.t_coll_comment.f_status == 'Approved')).select()
    except:
        response.title = 'Navigation Error'
        response.subtitle = 'Invalid collection'
        response.flash = 'Please use navigation from index to select a collecion'
   
    return locals()

def item_details():
#     redirect(URL('index'))
    itemId = request.vars['itemId']
    collection = request.vars['collection']
    try:
        item = db(db.geo_item.id == itemId).select().first()
        response.metatitle += " - " + item.f_name
        response.title = item.f_name
        response.subtitle = item.f_alt1
#         if item.f_alt2:
#             location = parse_text(item.f_alt)
        # if item.f_wiki:
        #     site = 'http://en.wikipedia.org/w/index.php?section=1&title=' + wiki_sub(item.f_wiki)
        #     wiki = wiki_open(site + '&printable=yes')
        comments = db((db.t_item_comment.f_item_id == itemId) & (db.t_item_comment.f_status == "Approved")).select()
    except:
        response.title = 'Navigation Error'
        response.subtitle = 'Invalid item'
        response.flash = 'Please use navigation from index to select an item'
    return locals()

@auth.requires_login()
def comments_dash():
    response.metatitle += ' - My Comments'
    response.title = 'My Comments'
    response.subtitle = 'Separated by type'
    db.t_item_comment.f_status.writable = False
    db.t_coll_comment.f_status.writable = False
    return dict()

# this is the view for the museum mural
def museum_mural():
    collectionId = request.vars['collectionId']
    try:
        collection = db(db.geo_collection.id == collectionId).select().first()
        response.metatitle += " - " + collection.f_name
        response.title = collection.f_name
        response.subtitle = collection.f_location
        featuredItems = db((db.geo_item.f_collection_id == collectionId) & (db.geo_item.f_featured == 1)).select()
        items = db(db.geo_item.f_collection_id == collectionId).select()
        comments=db((db.t_coll_comment.f_collection_id == collectionId) & (db.t_coll_comment.f_status == 'Approved')).select()
    except:
        response.title = 'Navigation Error'
        response.subtitle = 'Invalid collection'
        response.flash = 'Please use navigation from index to select a collecion'
    return locals()

# determining the max height for a collection of items to make flexbox more balanced between 3 columns
def find_max_height_collection(collections, colls, exhibit_items):
    session.maxHeightColException = "default"
    session.position = 'top'
    #declaring maxHeight to find average column size
    totalHeight = 0
    
    # get the height of each image
    for collection in collections:
        session.position = 'collections for loop'
        for item in exhibit_items:
            session.position = 'exhibit_items for loop'
            session.itemId = item
            session.collFI = collection.f_featured_img
            if item.id == collection.f_featured_img and item.id is not None:
                session.position = 'featured image if'
                #use PIL to open image and find height
                try:
                    thumb = Image.open(request.folder + 'uploads/thumbs/' + item.f_thumb)
                    session.thumbSize = thumb.size
                    # get the image height
                    (width, height) = thumb.size
                    totalHeight += height + 80
                    session.position = "try bottom"
                except Exception as e:
                    session.maxHeightColException = "there was a problem finding the image's height for " + e
    session.position = 'bottom'
    height = (totalHeight / colls) + 400
    session.height = height
    return height




def find_max_height(items, colls):
    session.itemCreateException = ""
    #declaring maxHeight to find average column size
    totalHeight = 0
    # get the height of each image
    for item in items:
        #use PIL to open image and find height
        if item.f_thumb is not None:
            try:
                thumb = Image.open(request.folder + 'uploads/thumbs/' + item.f_thumb)
                # get the image height
                (width, height) = thumb.size
                totalHeight += height + 80
            except Exception as e:
                session.itemCreateException = "there was a problem finding the image's height for " + e
    maxHeight = (totalHeight / colls) + 200
    session.maxHeight = maxHeight
    return maxHeight

# ## TODO: build tours ##
# def view_tours():
#     return dict()

# def tour_details():
#     return dict()


##### The following functions are used in wiki article retrieval and parsing #####
import urllib2
from HTMLParser import HTMLParser
import re
def wiki_open(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    infile = opener.open(url)
    info = infile.read()
    info = text_strip(info)
    return info

def wiki_sub(article):
    m = re.sub('(\s)','_',article)
    return m

# This class is used to strip all html from within the selection
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

# Seaches for first <p>, deletes HTML, and deletes [] reference tags
def text_strip(text):
    m = re.search('<p>(.*?)</p>', text)
    m = m.group(0)
    s = MLStripper()
    s.feed(m)
    m = s.get_data()
    m = re.sub('\[\d*\]', '', m)
    m = re.sub('\(\s*listen\s*\)', '', m)
    return m

# Function to parse location alt field into a URL compatible string
def parse_text(location):
    m = re.sub('(\W*\s)','+',location) # \W must have * due to python oddity in parsing the degree symbol
    return m
