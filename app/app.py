import swapi
import requests
import json
import asyncio
from flask import Flask, jsonify, request  
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from bson import json_util,ObjectId
from pymongo import MongoClient
from celery import Celery
# from flask_celery import make_celery
# from flask.ext.mongoalchemy import MongoAlchemy


class JSONEncoder(json.JSONEncoder): 
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'star_wars_db'
app.config['MONGO_URI'] = 'mongodb://isaiasgomes:isaiasgomes0@ds239931.mlab.com:39931/star_wars_db' #URI MLAB

# app.config['CELERY_BROKER_URL'] = 'ampq://localhost//'
# app.config['CELERY_BACKEND'] = 'mongodb://isaiasgomes:isaiasgomes0@ds239931.mlab.com:39931/star_wars_db' #URI MLAB
# app.config['MONGOALCHEMY_CONNECTION_STRING']= 'mongodb://isaiasgomes:isaiasgomes0@ds239931.mlab.com:39931/star_wars_db' #URI MLAB

# celery = make_celery(app)
mongo = PyMongo(app)

@app.route('/planeta', methods=['GET'])
def get_all(): 
    return jsonify({'planetas' : get_all_planets()})
    

@app.route('/planeta/id/<ObjectId:_id>', methods=['GET'])
@app.route('/planeta/id/<int:id>', methods=['GET'])
@app.route('/planeta/nome/<string:nome>', methods=['GET'])
def get_one(_id=None,id=None,nome=None):
    planeta = mongo.db.planeta 
    output = []

    if _id != None: 
        p = planeta.find_one({'_id' : _id})
        if p:
            output.append({'_id' :JSONEncoder().encode(p['_id']),'nome' : p['nome'], 'clima' : p['clima'], 'terreno' : p['terreno'],'quantidade de aparições em filmes: ' : 0 })
        else:
            output.append({'Erro':'Nenhum planeta encontrado'})
    if id != None:
        output = get_one_swapi(id,None)

    if nome != None:
        p = planeta.find_one({'nome' : nome})
        if p:
            output.append({'_id' :JSONEncoder().encode(p['_id']),'nome' : p['nome'], 'clima' : p['clima'], 'terreno' : p['terreno'],'quantidade de aparições em filmes: ' : 0 })
        else:
            output = get_one_swapi(None,nome)

    return jsonify({'result' : output})


@app.route('/planeta', methods=['POST'])
def add():
    planeta = mongo.db.planeta 

    nome = request.json['nome']
    clima = request.json['clima']
    terreno = request.json['terreno']
    
    planeta_id = planeta.insert({'nome' : nome, 'clima' : clima, 'terreno' : terreno})
    p = planeta.find_one({'_id' : planeta_id})
    
    output = JSONEncoder().encode(p)
    return output


@app.route('/planeta/<nome>', methods=['PUT'])
def update(nome):
    planeta = mongo.db.planeta 

    p = planeta.find_one({'nome' : nome})

    if p:
        data = request.get_json()
        planeta.update(p, {'$set': data})
        output = 'Planeta atualizado'
    else:
        output = 'Nenhum planeta encontrado'
    
    return jsonify({'result' : output})


@app.route('/planeta/<nome>', methods=['DELETE'])
def delete(nome):
    planeta = mongo.db.planeta 

    p = planeta.find_one({'nome' : nome})

    if p:
        planeta.remove(p)
        output = 'Planeta removido'
    else:
        output = 'Nenhum planeta encontrado'
    
    return jsonify({'result' : output})


def get_all_planets(): 
    result = []
    result.append(get_all_swapi())
    result.append(get_all_mongo())
    return result

def get_all_swapi():
    n = 1
    result = []
    mensagem = {'Erro':'Nenhum planeta encontrado'}
    #SWAPI
    planets = swapi.get_all("planets")
    for r in planets.order_by("created"):
        result.append({'_id':n,'nome':r.name,'clima':r.climate,'terreno':r.terrain,'quantidade de aparições em filmes: ' : len(r.films)})
        n+=1
    if len(result) == 0:
        return mensagem
    else:
        return result

def get_all_mongo():
    planeta = mongo.db.planeta
    result = []
    mensagem = {'Erro':'Nenhum planeta encontrado'}
    #MONGODB
    for p in planeta.find():
        result.append({'_id' :JSONEncoder().encode(p['_id']),'nome' : p['nome'], 'clima' : p['clima'], 'terreno' : p['terreno'],'quantidade de aparições em filmes: ' : 0 })
    
    if len(result) == 0:
        return mensagem
    else:
        return result




def get_one_swapi(id=None,nome=None): 
    n = 1
    output = []
    result = []
    mensagem = {'Erro':'Nenhum planeta encontrado'}
    #SWAPI
    planets = swapi.get_all("planets")
    for r in planets.order_by("created"):
        output.append({'_id':n,'nome':r.name,'clima':r.climate,'terreno':r.terrain,'quantidade de aparições em filmes: ' : len(r.films)})
        n+=1
    if id != None:
        for i in output:
            if i['_id'] == id:
                result.append({'_id':i['_id'],'nome':i['nome'],'clima':i['clima'],'terreno':i['terreno'],'quantidade de aparições em filmes: ': len(swapi.get_planet(i['_id']).films)})

    if nome != None:
        for i in output:
            if i['nome'] == nome:
                result.append({'_id':i['_id'],'nome':i['nome'],'clima':i['clima'],'terreno':i['terreno'],'quantidade de aparições em filmes: ': len(swapi.get_planet(i['_id']).films)})
    
    if len(result) == 0:
        return mensagem
    else:
        return result



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


