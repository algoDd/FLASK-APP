# GeoLocation Detection
Software can be used for GeoLocation Detection, it searches for given latitude longitude in the geo map json and returns the location where our latitude and longitude lie.

Language : Python

Framework Used :
Flask

### Step To Run:
- Install all required libraries ( sorry I don't have requirement txt anymore, Ill be happy if any of you can contribute )
- Run app.py
- open http://127.0.0.1:5000/


### APIS Docs :

#### (POST)
- http://127.0.0.1:5000/post_location
- Expected Json :
{ "pin": "", "place_name": "", "admin_name": "", "latitude": "", "longitude": "" }

#### (Get)
- http://127.0.0.1:5000/get_using_postgres?latitude=&longitude=

- http://127.0.0.1:5000/get_using_self?latitude=&longitude=

- http://127.0.0.1:5000/get_place?latitude=28.6333&longitude=77.2167
