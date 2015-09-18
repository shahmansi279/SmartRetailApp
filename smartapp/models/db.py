# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


db.define_table('users',
                 Field('uemail','string', requires=IS_NOT_EMPTY()),
                 Field('password','string',requires=IS_NOT_EMPTY()),
                 Field('role','string'),
                 Field('phone','string',requires=IS_NOT_EMPTY()),
                 Field('address','string',requires=IS_NOT_EMPTY()),
                 Field('zipcode','string',requires=IS_NOT_EMPTY()))


db.define_table('image',

   Field('title', unique=True),
   Field('picture', 'upload', uploadfield='picture_file'),
   Field('picture_file', 'blob'))


db.define_table('sensors',
                 Field('sensor_id','string'),
                 Field('sensor_type','string',requires=IS_NOT_EMPTY()),
                 Field('sensor_locn','string',requires=IS_NOT_EMPTY()),
                 Field('sensor_desc','string',requires=IS_NOT_EMPTY()),
                 Field('attr1','string'),
                 Field('attr2','string'))

db.define_table('places',
                 Field('place_id','string',requires=IS_NOT_EMPTY()),
                 Field('place_name','string',requires=IS_NOT_EMPTY()),
                 Field('place_desc','string',requires=IS_NOT_EMPTY()),
                 Field('place_addr','string',requires=IS_NOT_EMPTY()),
                 Field('place_timing','string'),
                 Field('place_lat','string'),
                 Field('place_long','string'),
                 Field('place_temp','string'),
                 Field('place_timing','string'),
                 Field('icon_image_id', 'reference image'),
                 Field('pl_img_id','reference image'))

db.define_table('events',
                 Field('event_id','string',requires=IS_NOT_EMPTY()),
                 Field('event_title','string',requires=IS_NOT_EMPTY()),
                 Field('event_desc','string',requires=IS_NOT_EMPTY()),
                 Field('event_addr','string',requires=IS_NOT_EMPTY()),
                 Field('event_timing','string'),
                 Field('ev_place_lat','string'),
                 Field('ev_place_long','string'),
                 Field('ev_place_id','reference places'),
                 Field('icon_image_id', 'reference image')
                 )

db.define_table('offers',

                 Field('offer_title','string',requires=IS_NOT_EMPTY()),
                 Field('offer_desc','string',requires=IS_NOT_EMPTY()),
                 Field('offer_validity','string'),
                 Field('offer_place_id','reference places'),
                 Field('icon_image_id', 'reference image')
                 )

db.define_table('beacons',
                 Field('beacon_id','string',requires=IS_NOT_EMPTY()),
                 Field('b_factory_id','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_name','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_desc','string',requires=IS_NOT_EMPTY()),
                 Field('b_place_id','string'),
                 Field('beacon_status','string'),
                 Field('beacon_lat','string'),
                 Field('beacon_long','string'),
                 Field('b_battery_lvl','string'))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.places.icon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.places.pl_img_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
