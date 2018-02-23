
# coding: utf-8

# In[1]:


from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import math
from sqlalchemy import text
import numpy as np
import json


# In[2]:


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/apitest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# @app.route('/post_location', methods=['POST'])
# def post_location():
#     con=config.connect()
#   

# In[3]:


db = SQLAlchemy(app)
class location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pin = db.Column(db.String(100))
    place_name = db.Column(db.String(50))  
    admin_name = db.Column(db.String(200))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    def api(self,pin,place_name,admin_name,latitude,longitude):
        self.pin=pin 
        self.place_name=place_name
        self.admin_name=admin_name
        self.latitude=latitude
        self.longitude=longitude


@app.route('/')
def show_all():
    return render_template('info.html')

@app.route('/post_location',methods=['POST'])
def post_location():
    req_data = request.get_json()
    pin = req_data['pin']
    place_name = req_data['place_name']
    admin_name = req_data['admin_name']
    latitude = req_data['latitude']
    longitude = req_data['longitude']
    if(pin=="" or place_name=="" or admin_name=="" or latitude=="" or longitude==""):
        return'Please Fill All Details'
    else:
	sql = text('Select pin from location where pin='+"'"+pin+"'")
    	result = db.engine.execute(sql)
	if(len(result.fetchall())==0):
		a=location()
        	a.api(pin,place_name,admin_name,latitude,longitude)
        	db.session.add(a)
        	db.session.commit()
        	return 'Data Saved'
	else:
        	return 'Data Exist'

@app.route('/get_using_postgres',methods=['GET'])
def get_using_postgres():
    longitude=request.args['longitude']
    latitude=request.args['latitude']
    radius= 5000
    sql = text('select pin from location WHERE earth_box(ll_to_earth('+latitude+","+longitude+'),5000.0) @> ll_to_earth(location.latitude, location.longitude)')
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])
        
    jsonname=json.dumps(names)
    return jsonname


@app.route('/get_using_self',methods=['GET'])
def get_using_self():
    #haversine formula
    lat=float(request.args['latitude'])
    lng=float(request.args['longitude'])
    radiusOfEarth = 6371
    latitude=[]
    longitude=[]
    pin=[]
    sql = text('Select latitude,longitude,pin from location')
    result = db.engine.execute(sql)
    for row in result:
        latitude.append(row[0])
        longitude.append(row[1])
        pin.append(row[2])
    latitude=np.matrix(latitude,dtype=float)
    longitude=np.matrix(longitude,dtype=float)
    pin=np.matrix(pin,dtype=str)
    dlat=(latitude-lat)*(np.pi/180)
    dlong=(longitude-lng)*(np.pi/180)
    first=np.square(np.sin(dlat/2))
    second1=np.multiply(np.cos(latitude*(np.pi/180)),np.cos((lat*(np.pi/180))))
    second2=np.square(np.sin(dlong/2))
    a=first+np.multiply(second1,second2)
    c=np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = np.multiply(radiusOfEarth,c)
    pin=pin[~np.isnan(d)]
    d=d[~np.isnan(d)]
    pin=pin[d<(5)]
    jsonpin=json.dumps(str(pin))
    return jsonpin
@app.route('/get_place',methods=['GET'])
def get_place():
	lat1=float(request.args['latitude'])
	lng1=float(request.args['longitude'])
	c=0
	sql = text('Select name , type , parent , coordinates from geojson')
	result = db.engine.execute(sql)
	name=[]
	typ=[]
	parents=[]
	coordinates=[]
	for row in result:
	    name.append(row[0])
	    typ.append(row[1])
 	    parents.append(row[2])
 	    coordinates.append(row[3])
    	def quadrant(w,lng1,lat1):
       		lng=w[:,0]
        	lat=w[:,1]
        	lenlat=np.median(lat,axis=0)
        	lenlng=np.median(lng,axis=0)
       	 	for i in range(1):
            		if lng1<=lenlng and lat1>=lenlat:
                #print '1st'
                		lng=lng[lng<=lenlng]
                		lat=lat[lat>=lenlat]
            		elif lng1>=lenlng and lat1>=lenlat:
                #print '2nd'
              			lng=lng[lng>=lenlng]
                		lat=lat[lat>=lenlat]
            		elif lng1<=lenlng and lat1<=lenlat:
                #print '3rd'
                		lng=lng[lng<=lenlng]
                		lat=lat[lat<=lenlat]
            		elif lng1>=lenlng and lat1<=lenlat:
                		lng=lng[lng>=lenlng]
                		lat=lat[lat<=lenlat]
                #print '4th'
            	return lng , lat
    
    	for i in range(len(name)):
     		   q=coordinates[i]
     		   w=np.matrix(q[0])
     		   lng,lat=quadrant(w,lng1,lat1)
     		   if c>1:
     			       lng,lat=quadrant(w,lng1,lat1)
      			       c=c-1
       		   xmax=lng.max()
       		   xmin=lng.min()
       		   ymax=lat.max()
       		   ymin=lat.min()
    #print xmax,xmin,ymin,ymax
       		   if(lng1<=xmax and lng1>=xmin and lat1<=ymax and lat1>=ymin):
       			     found=name[i]
          		     c=c+1
	if len(found)>0:
 	   return found
	else:
 	   return 'Not Found'
    
    

if __name__ == '__main__':
    app.run(port=5000,debug=True)#for debugging debug=True

