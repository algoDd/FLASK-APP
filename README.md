# apitest

API 1 (POST) :
http://127.0.0.1:5000/post_location

Expected Json :
{ "pin": "", "place_name": "", "admin_name": "", "latitude": "", "longitude": "" }

API 2 (GET 1) :
http://127.0.0.1:5000/get_using_postgres?latitude=&longitude=

API 2 (GET 2) :
http://127.0.0.1:5000/get_using_self?latitude=&longitude=
