# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
import gluon.contrib.simplejson as json

def register():

    uemail=request.vars.uemail
    password=request.vars.password
    phone=request.vars.phone
    address=request.vars.address
    zipcode=request.vars.zipcode
    code =412
    message="error"
    if uemail:
        if password :
            if phone :
                if address :
                    if zipcode:    
                        user_id=db.smartapp_users.insert(u_email=uemail,u_password=password,u_phone=phone,u_address1=address,u_zipcode=zipcode)
                        if user_id:
                                 message="success"
                                 code=200

    response.headers['Content-Type']='application/json'

    response.status=int(code)
    return json.dumps(dict(message=message))

def login():
    
    import cgi
    response.flash="Welcome"
    id=request.vars.uemail
    pwd=request.vars.password
    rows=db(db.smartapp_users.u_email==id).select(db.smartapp_users.u_password)

    if rows :
        message="invalid username"
        code=401
        if(str(rows[0].u_password)==pwd) :
            message="success"
            code=200
        else :
            message="invalid  password"
            code=401

    else :
       message="invalid username "
       code=401

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))


def authenticate(uemail, password):

    users= db((db.smartapp_users.u_email== uemail)&(db.smartapp_users.u_password==password)).select()
    if users:
        return True
    else:
        return False

def getuserrole(uemail):
    
  users= db((db.smartapp_users.u_email== uemail)).select(db.smartapp_users.u_role)
  if users:
        return users[0].u_role
  

def addplace():
    
    uemail=request.vars.uemail
    password=request.vars.password


    place_desc=request.vars.place_desc
    place_name=request.vars.place_name
    place_addr=request.vars.place_addr
    place_lat=""
    place_long=""

    valid_usr=authenticate(uemail,password)
    if valid_usr:
        usr_role=getuserrole(uemail)
    
        if(usr_role=="admin"):

        #insert into gimbal server and get place-id , place_lat, place_long
          

            import urllib, urllib2, base64

            data={"name":place_name}
            data_json = json.dumps(data)
            headers = {
             'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
             'Content-Type': 'application/json'
             }
            req = urllib2.Request(
            'https://manager.gimbal.com/api/v2/places',data_json, headers)
            res=json.load(urllib2.urlopen(req))
            place_id=res["id"]

            #insert into datastore

            pl_id=db.smartapp_places.insert(pl_id=place_id,pl_desc=place_desc,pl_name=place_name,pl_address1=place_addr,pl_lat=place_lat,
                              pl_long=place_long)
            
            if(pl_id) :
                code=200
                
                message="success"
                return json.dumps(dict(message=message))
            else :
                code=412
         
                message="error"
              
         
        else:
          code=401
          message="user not authorized"

    else:
            code=412
            message="User not Authenticated"

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))

def getplace():

    # From Directly Gimbal
    import urllib, urllib2, base64
    
    uemail=request.vars.uemail
    password=request.vars.password

    valid_usr=authenticate(uemail,password)
    if valid_usr:

        headers = {
         'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
         'Content-Type': 'application/json'
         }
        req = urllib2.Request(
        'https://manager.gimbal.com/api/v2/places',
        None, headers)

        code=200
        response.headers['Content-Type']='application/json'
        response.status=int(code)
        return urllib2.urlopen(req).read()
    
    else:
        code=412
        response.headers['Content-Type']='application/json'
        response.status=int(code)
        return json.dumps(dict(message="error"))
        

def getevents():

    uemail=request.vars.uemail
    password=request.vars.password
    place_id=request.vars.place_id

    valid_usr=authenticate(uemail,password)
    if valid_usr:
      #From Datastore
        rows = db(db.smartapp_events.event_place_id==place_id).select()
        code=200
        response.headers['Content-Type']='application/json'
        response.status=int(code)

        return json.dumps([{'event_id':r.event_id,'event_title':r.event_title,'event_desc':r.event_desc,'ev_place_lat':r.event_place_lat,'ev_place_long':r.event_place_long,'event_addr':r.event_address1,'icon_img_id':r.icon_image_id,'ev_place_id':r.event_place_id,'event_timing':r.event_timing,'ev_img_url':getimage(r.icon_image_id)} for r in rows])
    else :
        code=412
        response.headers['Content-Type']='application/json'
        response.status=int(code)
        return json.dumps(dict(message='error'))



def getplaces():

    uemail=request.vars.uemail
    password=request.vars.password

    valid_usr=authenticate(uemail,password)
    if valid_usr:
      #From Datastore
        rows = db(db.smartapp_places.id>0).select()
        code=200
        response.headers['Content-Type']='application/json'
        response.status=int(code)

        return json.dumps([{'id':r.pl_id,'id_p':r.id,'name':r.pl_name,'place_desc':r.pl_desc,'place_lat':r.pl_lat,'place_long':r.pl_long,'place_addr':r.pl_address1,'pl_img_id':r.pl_icon_image_id,'pl_img_url':getimage(r.pl_icon_image_id),'pl_timing':r.pl_timing} for r in rows])
    else :
        code=412
        response.headers['Content-Type']='application/json'
        response.status=int(code)
        return json.dumps(dict(message='error'))

def addbeacon():

    uemail=request.vars.uemail
    password=request.vars.password


    beacon_name=request.vars.beacon_name
    b_factory_id=request.vars.b_factory_id
    beacon_lat=""
    beacon_long=""
    beacon_status="Active"

    valid_usr=authenticate(uemail,password)
    if valid_usr:
        usr_role=getuserrole(uemail)
    
        if(usr_role=="admin"):

        #insert into gimbal server and get place-id , place_lat, place_long
          

            import urllib, urllib2, base64

            data={"name":beacon_name,"factory_id":b_factory_id}
            data_json = json.dumps(data)
            headers = {
             'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
             'Content-Type': 'application/json'
             }
            req = urllib2.Request(
            'https://manager.gimbal.com/api/beacons',data_json, headers)
            res=json.load(urllib2.urlopen(req))
            beacon_id=res["id"]
            b_battery_lvl=res["battery_level"]
            #insert into datastore

            b_id=db.smartapp_beacons.insert(beacon_id=beacon_id,beacon_name=beacon_name,beacon_factory_id=b_factory_id,beacon_lat=beacon_lat,beacon_long=beacon_long,beacon_status=beacon_status,beacon_battery_lvl=b_battery_lvl)


            if(b_id) :

                message="success"
                return json.dumps(dict(message=message))
            else :
                code=412

                message="error"

        else:
          code=401
          message="user not authorized"

    else:
            code=412
            message="User not Authenticated"

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))


    return None

def activateBeacon():

    uemail=request.vars.uemail
    password=request.vars.password

    b_name=request.vars.b_name
    b_f_id=request.vars.b_f_id

    valid_usr=authenticate(uemail,password)
    if valid_usr:
        usr_role=getuserrole(uemail)
    
        if(usr_role=="admin"):

     
            import urllib, urllib2, base64

            data={"name":b_name,"factory_id":b_f_id}
            data_json = json.dumps(data)
            headers = {
             'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
             'Content-Type': 'application/json'
             }
            req = urllib2.Request(
            'https://manager.gimbal.com/api/beacons',data_json, headers)
            res=json.load(urllib2.urlopen(req))

            if(res) :
                code=200
                rows =db (db.beacons.b_factory_id==b_f_id).select()
                if rows:
                    for row in rows:
                      row.update_record(beacon_status="Active")
                
                message="success"
                return json.dumps(dict(message=message))
            else :
                code=412
         
                message="error"
              
         
        else:
          code=401
          message="user not authorized"

    else:
            code=412
            message="User not Authenticated"

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))

    return None

def getallbeacons():

    uemail=request.vars.uemail
    password=request.vars.password

    valid_usr=authenticate(uemail,password)
    if valid_usr:
      #From Datastore
        rows = db(db.beacons.id>0).select()
        code=200
        response.headers['Content-Type']='application/json'
        response.status=int(code)

        return json.dumps([{'id':r.beacon_id,'b_f_id':r.beacon_factory_id,'name':r.beacon_name,'beacon_desc':r.beacon_desc,'beacon_lat':r.beacon_lat,'beacon_long':r.beacon_long,'beacon_status':r.beacon_status,'b_place_id':r.beacon_place_id,'b_battery_lvl':r.beacon_battery_lvl}for r in rows])
    else :
        code=412
        response.headers['Content-Type']='application/json'
        response.status=int(code)
        return json.dumps(dict(message='error'))

    return None

def deActivateBeacon():
    
    uemail=request.vars.uemail
    password=request.vars.password

    b_f_id=request.vars.b_f_id

    valid_usr=authenticate(uemail,password)
    if valid_usr:
        usr_role=getuserrole(uemail)
    
        if(usr_role=="admin"):

        #insert into gimbal server and get place-id , place_lat, place_long
          

            import urllib, urllib2, base64

            
            headers = {
             'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
             'Content-Type': 'application/json'
             }
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            url="https://manager.gimbal.com/api/beacons/"+b_f_id
            req = urllib2.Request(
            url,None, headers)
            req.get_method =lambda: 'DELETE'
            res=opener.open(req)
            
                       
            
            if(res) :
                code=200

                rows =db (db.beacons.b_factory_id==b_f_id).select()
                if rows:
                    for row in rows:
                      row.update_record(beacon_status="DeActivated")

                    message="success"
                    return json.dumps(dict(message=message))
            else :
                code=412
         
                message="error"
              
         
        else:
          code=401
          message="user not authorized"

    else:
            code=412
            message="User not Authenticated"

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))

    return None

    

def updateBeacon():
    
    uemail=request.vars.uemail
    password=request.vars.password
    b_f_id=request.vars.b_f_id
    b_name=request.vars.b_name

    valid_usr=authenticate(uemail,password)
    if valid_usr:
        usr_role=getuserrole(uemail)
    
        if(usr_role=="admin"):

        #insert into gimbal server and get place-id , place_lat, place_long
          

            import urllib, urllib2, base64,httplib

            data={"name":b_name}
            data_json = json.dumps(data)
            headers = {
             'Authorization': 'Token token=f50ccc1aab3314434ae32dada87312cb',
             'Content-Type': 'application/json'
             }
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            url="https://manager.gimbal.com/api/beacons/"+b_f_id
            req = urllib2.Request(
            url,data_json, headers)
            req.get_method =lambda: 'PUT'
            res=opener.open(req)

           
            
            if(res) :
                code=200
                rows =db (db.beacons.b_factory_id==b_f_id).select()
                if rows:
                    for row in rows:
                      row.update_record(beacon_name=b_name)
                message="success"
                return json.dumps(dict(message=message))
            else :
                code=412
         
                message="error"
              
         
        else:
          code=401
          message="user not authorized"

    else:
            code=412
            message="User not Authenticated"

    response.headers['Content-Type']='application/json'
    response.status=int(code)
    return json.dumps(dict(message=message))

    return None

def getimage(img_id):
    imgid=  img_id
    imagename= db((db.image.id== imgid)).select(db.image.picture)
    imagename[0].picture
    url=imagename[0].picture
    return url

def getplaceid(place_id):
  
    pl_id=  place_id
    placeid= db((db.smartapp_places.pl_id== pl_id)).select()
    
  
    return placeid[0].id

def getoffer():
   place_id=request.vars.place_id
   placeid=getplaceid(place_id)
   rows= db(db.smartapp_offers.offer_place_id== placeid).select()
    
   return json.dumps([{'id':r.id,'offer_title':r.offer_title,'offer_desc':r.offer_desc,'offer_place_id':r.offer_place_id,'offer_validity':r.offer_validity_ends,'offer_img_url':getimage(r.icon_image_id)}for r in rows])

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
