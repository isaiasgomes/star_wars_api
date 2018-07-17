# star_wars_api
A simple REST Api using Flask-Restful and MongoDB and comparing data with https://swapi.co/ . The Api supports get, put, post and delete functions and has endpoints for get name and id requests.

Production environment end-points:

get all 
http://34.230.239.81/planeta

get one by id 
http://34.230.239.81/planeta/id/1

get one by ObjectId 
http://34.230.239.81/planeta/id/5b4e6b7926e2077fdad60a3f

get one by name
http://34.230.239.81/planeta/nome/Terra

post a planet
http://34.230.239.81/planeta
{"nome":"Saturno","clima":"frio","terreno":"irregular"}

put a planet 
http://34.230.239.81/planeta/Saturno
{"nome":"Saturno","clima":"gelado","terreno":"irregular"}

delete
http://34.230.239.81/planeta/Saturno







