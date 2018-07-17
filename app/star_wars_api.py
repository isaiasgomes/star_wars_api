import swapi
import requests
import json
from flask import Flask, jsonify, request  
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from bson import json_util
from bson import ObjectId
from pymongo import MongoClient


class JSONEncoder(json.JSONEncoder): 
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'star_wars_db'
app.config['MONGO_URI'] = 'mongodb://isaiasgomes:isaiasgomes0@ds239931.mlab.com:39931/star_wars_db' #URI MLAB

mongo = PyMongo(app)

@app.route('/planeta', methods=['GET'])
def get_all(): 
    planeta = mongo.db.planeta 
    output = []
    i = 1
    #SWAPI
    planets = swapi.get_all("planets")
    for r in planets.order_by("created"):
        output.append({'_id':i,'nome':r.name,'clima':r.climate,'terreno':r.terrain,'quantidade de aparições em filmes: ' : len(r.films)})
        i+=1
    #MONGODB
    for p in planeta.find():
        output.append({'_id' :JSONEncoder().encode(p['_id']),'nome' : p['nome'], 'clima' : p['clima'], 'terreno' : p['terreno'],'quantidade de aparições em filmes: ' : 0 })

        #output = JSONEncoder().encode(p)
    #return output
    return jsonify({'planetas' : output})
    

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
    
    #output = {'_id' : planeta_id,'nome' : p['nome'], 'clima' : p['clima'], 'terreno' : p['terreno'] }
    output = JSONEncoder().encode(p)
    return output
    #return jsonify({'result' : output})


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


