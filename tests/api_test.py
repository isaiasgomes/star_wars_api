import unittest
import requests


class Test_Star_Wars_API(unittest.TestCase):

    def test_get_planet_swapi_id(self):
        endpoint = "http://127.0.0.1:5000/planeta/id/1"
        vetor = self.get(endpoint)
        for v in vetor:
            self.assertEquals(v['nome'], "Tatooine")

    def test_get_planet_mongo_id(self):
        endpoint = "http://127.0.0.1:5000/planeta/id/5b4e17f0ee9b680532b90f2f"
        vetor = self.get(endpoint)
        for v in vetor:
            self.assertEquals(v['nome'], "Mercúrio")

    def test_get_planet_swapi_name(self):
        endpoint = "http://127.0.0.1:5000/planeta/nome/Tatooine"
        vetor = self.get(endpoint)
        for v in vetor:
            self.assertEquals(v['nome'], "Tatooine")
    
    def test_get_planet_mongo_name(self):
        endpoint = "http://127.0.0.1:5000/planeta/nome/Saturno"
        vetor = self.get(endpoint)
        for v in vetor:
            self.assertEquals(v['nome'], "Saturno")
    
    def test_post_planet(self):
        endpoint = "http://127.0.0.1:5000/planeta"
        status_code = self.post(endpoint)
        self.assertEquals(status_code, 200)
    
    def test_delete_planet(self):
        endpoint = "http://127.0.0.1:5000/planeta/Saturno"
        status_code = self.delete(endpoint)
        self.assertEquals(status_code, 200)
    



    def get(self,endpoint): 
        vetor = []
        response = requests.get(endpoint)
        data = response.json()
        for result in data['result']:
            vetor.append(result)
        return vetor


    def post(self, endpoint): 
        data_post = {'nome':'Saturno','clima':'gasoso e tempestivo','terreno':'irregular'}
        response = requests.post(endpoint, json=data_post)
        return response.status_code


    def delete(self,endpoint): 
        response = requests.delete(endpoint)
        return response.status_code


            

        



