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

db.define_table('smartapp_users', Field('u_fname','string', requires=IS_NOT_EMPTY()),
                 Field('u_lname','string', requires=IS_NOT_EMPTY()),
                 Field('u_email','string', requires=IS_NOT_EMPTY()),
                 Field('u_password','string',requires=IS_NOT_EMPTY()),
                 Field('u_phone','string',requires=IS_NOT_EMPTY()),
                 Field('u_alt_phone1','string'),
                 Field('u_alt_phone2','string'),
                 Field('u_address1','string',requires=IS_NOT_EMPTY()),
                 Field('u_address2','string'),
                 Field('u_city','string',requires=IS_NOT_EMPTY()),
                 Field('u_state','string',requires=IS_NOT_EMPTY()),
                 Field('u_zipcode','string',requires=IS_NOT_EMPTY()),
                 Field('u_role','string'),
                 Field('u_account_status','string',requires=IS_NOT_EMPTY()),
                 Field('u_activation_date','datetime'),
                 Field('u_deactivation_date','datetime'),
                 Field('u_pref_payment_method','string',requires=IS_NOT_EMPTY()),
                 Field('u_creditcard_type','string'),
                 Field('u_creditcard_number','integer'),
                 Field('u_creditcard_exp_month','integer'),
                 Field('u_creditcard_exp_year','integer'),
                 Field('u_creditcard_code','integer'),
                 Field('u_attr1','string'),
                 Field('u_attr2','string'),
                 Field('u_attr3','string'),
                 Field('u_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('u_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('u_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('u_last_update_by','string',requires=IS_NOT_EMPTY()))

db.define_table('image',
                  Field('title', unique=True),
                  Field('picture', 'upload', uploadfield='picture_file'),
                  Field('picture_file', 'blob'))

db.define_table('smartapp_beacons',
                 Field('beacon_id','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_factory_id','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_name','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_desc','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_type','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_place_id','string'),
                 Field('beacon_locn','string',requires=IS_NOT_EMPTY()),
	             Field('beacon_status','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_lat','string'),
                 Field('beacon_long','string'),
                 Field('beacon_make','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_model','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_year','string',requires=IS_NOT_EMPTY()),
               Field('beacon_image_id', 'reference image'),
                 Field('beacon_activation_date','datetime'),
                 Field('beacon_deactivation_date','datetime'),
                 Field('beacon_recall_status','string', requires=IS_NOT_EMPTY()),
                 Field('beacon_recall_date','date'),
                 Field('beacon_battery_type','string', requires=IS_NOT_EMPTY()),
                 Field('beacon_battery_lvl','string'),
                 Field('beacon_battery_changed_date','date'),
                 Field('attr1','string'),
                 Field('attr2','string'),
                 Field('attr3','string'),
                 Field('beacon_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('beacon_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('beacon_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('beacon_last_update_by','string',requires=IS_NOT_EMPTY()))

db.define_table('smartapp_places', 
                 Field('pl_id','string',requires=IS_NOT_EMPTY()),
                 Field('pl_name','string',requires=IS_NOT_EMPTY()),
                 Field('pl_desc','string',requires=IS_NOT_EMPTY()),
                 Field('pl_type','string',requires=IS_NOT_EMPTY()),
                 Field('pl_place_attrib1','string',requires=IS_NOT_EMPTY()),
                 Field('pl_place_attrib2','string'),
                 Field('pl_place_attrib3','string'),
                 Field('pl_place_attrib4','string'),
                 Field('pl_timing','string'),
                 Field('pl_orders_email','string', requires=IS_NOT_EMPTY()),
                 Field('pl_contact_email','string', requires=IS_NOT_EMPTY()),
                 Field('pl_phone','string',requires=IS_NOT_EMPTY()),
                 Field('pl_alt_phone1','string'),
                 Field('pl_alt_phone2','string'),
                 Field('pl_address1','string',requires=IS_NOT_EMPTY()),
                 Field('pl_address2','string'),
                 Field('pl_city','string',requires=IS_NOT_EMPTY()),
                 Field('pl_state','string',requires=IS_NOT_EMPTY()),
                 Field('pl_zipcode','string',requires=IS_NOT_EMPTY()),
                 Field('pl_website_url','string'),
                 Field('pl_lat','string'),
                 Field('pl_long','string'),
                 Field('pl_temp','string'),
                 Field('pl_humidity','string'),
                 Field('pl_other_attr1','string'),
                 Field('pl_other_attr2','string'),
                 Field('pl_other_attr3','string'),
                 Field('pl_star_rating','string',requires=IS_NOT_EMPTY()),
                 Field('pl_accepted_payment_methods','string',requires=IS_NOT_EMPTY()),
                 Field('pl_accepted_payment_LOGO','blob'),
                 Field('pl_member_club1','string'),
                 Field('pl_member_club2','string'),
                 Field('pl_member_club3','string'),
                 Field('pl_icon_image_id', 'reference image'),
                 Field('pl_place_status','string',requires=IS_NOT_EMPTY()),
                 Field('pl_activation_date','datetime'),
                 Field('pl_deactivation_date','datetime'),
                 Field('pl_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('pl_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('pl_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('pl_last_update_by','string',requires=IS_NOT_EMPTY()))

db.define_table('smartapp_events',
                 Field('event_id','string',requires=IS_NOT_EMPTY()),
                 Field('event_title','string',requires=IS_NOT_EMPTY()),
                 Field('event_desc','string',requires=IS_NOT_EMPTY()),
                 Field('event_timing','string'),
                 Field('event_website_url','string'),
                 Field('event_attrib1','string',requires=IS_NOT_EMPTY()),
                 Field('event_attrib2','string'),
                 Field('event_attrib3','string'),
                 Field('event_attrib4','string'),
                 Field('event_subscription_email','string', requires=IS_NOT_EMPTY()),
                 Field('event_contact_email','string', requires=IS_NOT_EMPTY()),
                 Field('event_address1','string',requires=IS_NOT_EMPTY()),
                 Field('event_address2','string'),
                 Field('event_city','string',requires=IS_NOT_EMPTY()),
                 Field('event_state','string',requires=IS_NOT_EMPTY()),
                 Field('event_zipcode','string',requires=IS_NOT_EMPTY()),
                 Field('event_phone','string',requires=IS_NOT_EMPTY()),
                 Field('event_alt_phone1','string'),
                 Field('event_alt_phone2','string'),
                 Field('event_place_lat','string'),
                 Field('event_place_long','string'),
                 Field('event_place_id','reference smartapp_places'),
                 Field('event_other_attr1','string'),
                 Field('event_other_attr2','string'),
                 Field('event_other_attr3','string'),
                 Field('event_accepted_payment_methods','string',requires=IS_NOT_EMPTY()),
                 Field('event_accepted_payment_LOGO','blob'),
                 Field('event_member_club1','string'),
                 Field('event_member_club2','string'),
                 Field('event_member_club3','string'),
                 Field('event_star_rating','string'),
                 Field('event_status','string',requires=IS_NOT_EMPTY()),
                 Field('event_subscription_status','string',requires=IS_NOT_EMPTY()),
                 Field('event_subscription_status_desc','string',requires=IS_NOT_EMPTY()),
                 Field('icon_image_id', 'reference image'),
                 Field('event_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('event_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('event_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('event_last_update_by','string',requires=IS_NOT_EMPTY()))

db.define_table('smartapp_offers',
                 Field('offer_id','string',requires=IS_NOT_EMPTY()),
                 Field('offer_title','string',requires=IS_NOT_EMPTY()),
                 Field('offer_desc','string',requires=IS_NOT_EMPTY()),
                 Field('offer_validity_starts','string'),
                 Field('offer_validity_ends','string'),
                 Field('offer_website_url','string'),
                 Field('offer_status','string',requires=IS_NOT_EMPTY()),
                 Field('offer_place_id','reference smartapp_places'),
                 Field('offer_attrib1','string',requires=IS_NOT_EMPTY()),
                 Field('offer_attrib2','string'),
                 Field('offer_attrib3','string'),
                 Field('offer_attrib4','string'),
                 Field('offer_subscription_email','string', requires=IS_NOT_EMPTY()),
                 Field('offer_contact_email','string', requires=IS_NOT_EMPTY()),
                 Field('offer_phone','string'),
                 Field('offer_place_lat','string'),
                 Field('offer_place_long','string'),
                 Field('offer_other_attr1','string'),
                 Field('offer_other_attr2','string'),
                 Field('offer_other_attr3','string'),
                 Field('offer_accepted_payment_methods','string',requires=IS_NOT_EMPTY()),
                 Field('offer_accepted_payment_LOGO','blob'),
                 Field('offer_member_club1','string'),
                 Field('offer_member_club2','string'),
                 Field('offer_member_club3','string'),
                 Field('offer_star_rating','string'),
                 Field('offer_subscription_status','string',requires=IS_NOT_EMPTY()),
                 Field('offer_subscription_status_desc','string',requires=IS_NOT_EMPTY()),
                 Field('icon_image_id', 'reference image'),
                 Field('offer_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('offer_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('offer_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('offer_last_update_by','string',requires=IS_NOT_EMPTY()))

db.define_table('smartapp_indoormaps', 
                 Field('pl_id','string',requires=IS_NOT_EMPTY()),
                 Field('pl_name','string',requires=IS_NOT_EMPTY()),
                 Field('pl_desc','string',requires=IS_NOT_EMPTY()),
                 Field('pl_type','string',requires=IS_NOT_EMPTY()),
                 Field('pl_place_attrib1','string',requires=IS_NOT_EMPTY()),
                 Field('pl_place_attrib2','string'),
                 Field('pl_place_attrib3','string'),
                 Field('pl_place_attrib4','string'),
                 Field('pl_address1','string',requires=IS_NOT_EMPTY()),
                 Field('pl_address2','string'),
                 Field('pl_city','string',requires=IS_NOT_EMPTY()),
                 Field('pl_state','string',requires=IS_NOT_EMPTY()),
                 Field('pl_zipcode','string',requires=IS_NOT_EMPTY()),
                 Field('pl_lat','string'),
                 Field('pl_long','string'),
                 Field('pl_other_attr1','string'),
                 Field('pl_other_attr2','string'),
                 Field('pl_other_attr3','string'),
                 Field('pl_icon_image_id', 'reference image'),
                 Field('pl_place_status','string',requires=IS_NOT_EMPTY()),
                 Field('pl_activation_date','datetime'),
                 Field('pl_deactivation_date','datetime'),
                 Field('pl_creation_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('pl_created_by','string',requires=IS_NOT_EMPTY()),
                 Field('pl_last_update_date','datetime',requires=IS_NOT_EMPTY()),
                 Field('pl_last_update_by','string',requires=IS_NOT_EMPTY()))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.smartapp_places.pl_icon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.smartapp_indoormaps.pl_icon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.smartapp_beacons.beacon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.smartapp_events.icon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.smartapp_offers.icon_image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
#db.smartapp_places.pl.img_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
