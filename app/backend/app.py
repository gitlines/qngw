import requests
from urllib import parse
from flask import Flask, json
from flask_restful import Resource, Api, reqparse
import pprint
import pymongo
import random

from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)


class FindCityById(Resource):

    def __init__(self):

        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?id='
        self.metric = '&units=metric'
        self.kelvin = '&units=kelvin'
        self.lang = '&lang=de'
        self.key = '&appid=7c05094a7b12e6bdc0c3a720d230b2a0'
        self.full_url = ""

    def get(self):
        """
        Find a city by ID
        :return:
        """

        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='An ID needs to be provided.')
        args = parser.parse_args()

        # randomize temperature unit
        choose = [self.metric, self.kelvin]
        units = random.choice(choose)

        # encode the search term and build full url
        formatted_search_term = parse.quote(args.id)
        self.full_url = f"{self.base_url}{formatted_search_term}{units}{self.lang}{self.key}"

        # save the response of the request
        response = requests.get(self.full_url)
        # print(response.headers)
        # print('\nresponse: ' + response.text + '\n')

        if response.status_code == 200:
            # TODO: handle response
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')

        data = response.json()
        city_data = {
            'city_id': data['id'],
            'selected': True,
            'name': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp']
        }
        return city_data


class FindCityByName(Resource):

    def __init__(self):
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?q='
        self.metric = '&units=metric'
        self.kelvin = '&units=kelvin'
        self.lang = '&lang=de'
        self.key = '&appid=7c05094a7b12e6bdc0c3a720d230b2a0'
        self.full_url = ""

    def get(self):
        """
        Find a city by name
        :return:
        """

        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True, help='A city needs to be provided.')
        args = parser.parse_args()

        # randomize temperature unit
        choose = [self.metric, self.kelvin]
        units = random.choice(choose)

        # encode the search term and build full url
        formatted_search_term = parse.quote(args.city)
        self.full_url = f"{self.base_url}{formatted_search_term}{units}{self.lang}{self.key}"

        # save the response of the request
        response = requests.get(self.full_url)
        # print(response.headers)
        # print('\nresponse: ' + response.text + '\n')

        if response.status_code == 200:
            # TODO: handle response
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')

        data = response.json()
        city_data = {
            'city_id': data['id'],
            'selected': True,
            'name': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp']
        }
        return city_data


class ManageCities(Resource):

    def __init__(self):

        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?id='
        self.metric = '&units=metric'
        self.kelvin = '&units=kelvin'
        self.lang = '&lang=de'
        self.key = '&appid=7c05094a7b12e6bdc0c3a720d230b2a0'
        self.full_url = ""

    def get(self):
        """
        Get all cities from database
        :return:
        """

        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='A city needs to be provided.')
        args = parser.parse_args()

        # encode the search term and build full url
        formatted_search_term = parse.quote(args.id)

        # randomize temperature unit
        choose = [self.metric, self.kelvin]
        units = random.choice(choose)
        # print(random.choice(units))

        self.full_url = f"{self.base_url}{formatted_search_term}{units}{self.lang}{self.key}"

        print('\nfull URL: ' + self.full_url + '\n')

        # save the response of the request
        response = requests.get(self.full_url)

        print(response.headers)
        print('\nresponse: ' + response.text + '\n')

        if response.status_code == 200:
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')

        data = response.json()
        city_data = {
            'city_id': data['id'],
            'selected': True,
            'name': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp']
        }

        return city_data

    def post(self):
        """
        Adds the selected city to the database
        add city, country, id, and temperature
        :return:
        """

        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?q='

        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True, help='A city needs to be provided.')
        args = parser.parse_args()
        formatted_search_term = parse.quote(args.city)

        # randomize temperature unit
        choose = [self.metric, self.kelvin]
        units = random.choice(choose)
        # print(random.choice(units))

        self.full_url = f"{self.base_url}{formatted_search_term}{units}{self.lang}{self.key}"

        print('\nfull URL: ' + self.full_url + '\n')

        # save the response of the request
        response = requests.get(self.full_url)

        if response.status_code == 200:
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')

        data = response.json()

        # ---
        city_data = {
            'city_id': data['id'],
            'selected': True,
            'name': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp']
        }

        # check if the city is already in the database
        print('test')
        exists = db.add_city(city_data)

        print(f"exists with oid: {exists}")
        if exists:

            custom_msg = {
                'status': 'failure',
                'message': f"City with name: '{data['name']}' already exists",
            }
            city_data['msg'] = custom_msg
            response = app.response_class(
                response=json.dumps(city_data),
                # https://stackoverflow.com/questions/3825990/http-response-code-for-post-when-resource-already-exists
                status=409,
                mimetype='application/json'
            )

            print(f"resp: {response}")
            print(f"type of the resp: {type(response)}")
            return response
        else:
            custom_msg = {
                'status': 'success',
                'message': f"City with name: '{data['name']}' was added to the database",
            }
            city_data['msg'] = custom_msg

            response = app.response_class(

                response=json.dumps(city_data, indent=4, default=json_util.default),
                status=201,
                mimetype='application/json'
            )
            # print(f"resp: {response}")
            # print(f"type of the resp: {type(response)}")
            return response

    def put(self):
        """
        refresh temp data of all cites currently in table -- put you should not
        simply send an array with id's put querry the database inseta - the schema should have a selected bolean value
        :return:
        """

    def delete(self):
        """
        maybe this should be put as we could leave the city in the db, just not show it anymore
        :return:
        """


class DB(object):

    def __init__(self):
        # client = pymongo.MongoClient('mongodb://localhost:27017')
        client = pymongo.MongoClient('mongodb://root:admin@db:27017/')

        # self.db = client.get_database()
        self.db = client.weather_data  # specify db
        print('db:: ' + str(self.db))
        self.cities_coll = self.db.cities  # specify collection

        self.metric = '&units=metric'
        self.kelvin = '&units=kelvin'
        self.lang = '&lang=de'
        self.base_url = 'http://api.openweathermap.org/data/2.5/group?id='  # 524901,703448,2643743&units=metric'
        self.key = '&appid=7c05094a7b12e6bdc0c3a720d230b2a0'
        self.full_url = ""

    def add_city(self, data):

        if self.cities_coll.count_documents({'city_id': data['city_id']}, limit=1):
            return True

        else:
            # the returned document contains an "_id", which was automatically added on insert
            _id = self.cities_coll.insert(data)
            # print('Added City: {0}'.format(db_object))
            # print(f"id type: {type(_id)}")
            # print(f"id : {_id}")
            return False

    def get_city_by_name(self, data):

        return self.cities_coll.find_one({'name': data['name'], 'country': data['country']})

    def get_city_by_db_id(self, _id):

        return self.cities_coll.find_one({'_id': _id})

    def get_city_by_city_id(self, city_id):

        city_data = self.cities_coll.find_one({'city_id': city_id})

        if city_data:
            return city_data
        else:
            return None

    def get_all_cities_from_db(self):

        data = self.cities_coll.find({})

        for item in data:
            pprint.pprint(item)
        # pprint.pprint(list(data))

        return data

    def update_all(self):

        all_cities = self.get_all_cities_from_db()
        all_city_ids = self.cities_coll.distinct('city_id')
        print(all_city_ids)
        print(type(all_city_ids))

        city_ids = ",".join(map(str, all_city_ids))
        print(city_ids)

        # request to fetch all cities from the weather API
        self.full_url = f"{self.base_url}{city_ids}{self.metric}{self.lang}{self.key}"

        response = requests.get(self.full_url)

        # print(response.headers)
        # print('\nresponse: ' + response.text + '\n')
        #
        # if response.status_code == 200:
        #     print('Success!')
        # elif response.status_code == 404:
        #     print('Not Found.')

        data = response.json()

        # update temperature information
        for item, city in zip(data, all_cities):
            city["temp"] = item['main']['temp']
            self.cities_coll.replace_one({'city_id': city['city_it']}, city)

    def remove_city(self, _id):

        return self.cities_coll.remove({'_id': ObjectId(_id)})

    def remove_all(self):

        return self.cities_coll.drop()

    def create_initial_cities(self):

        # Moscow, Dublin, London, Wien, Paris, Berlin, Rom, Madrid, Brüssel, Amsterdam
        city_ids = "524901,2964574,2643743,2761369,2988507,2950159,6539761,3117735,2800866,2759794"
        self.full_url = f"{self.base_url}{city_ids}{self.metric}{self.lang}{self.key}"

        response = requests.get(self.full_url)

        # print(response.headers)
        # print('\nresponse: ' + response.text + '\n')
        #
        # if response.status_code == 200:
        #     print('Success!')
        # elif response.status_code == 404:
        #     print('Not Found.')

        data = response.json()

        # pprint.pprint(data)

        cities_data = []
        for item in data['list']:
            city_detail = {
                'city_id': item['id'],
                'selected': True,
                'name': item['name'],
                'country': item['sys']['country'],
                'temp': item['main']['temp']
            }
            cities_data.append(city_detail)
        # pprint.pprint(f"{cities_data}")
        print(type(cities_data))
        result = self.cities_coll.insert_many(cities_data)
        print(result)


db = DB()

# add all the endpoints as resources
api.add_resource(FindCityByName, '/api/city_search')
api.add_resource(ManageCities, '/api/manage_city')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8081)
