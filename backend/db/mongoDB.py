import pprint
import pymongo


class DB(object):

    def __init__(self):
        client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = client.cities

    def add_city(self, data):

        city_id = self.get_city_by_city_id(data['id'])

        if not city_id:

            city_data = {
                'city_id': city_id,
                'selected': True,
                'name': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp']
            }

            cities = self.db.cities
            db_object = cities.insert(city_data)
            print('Added City: {0}'.format(db_object))
            return db_object

        else:

            response = {
                'status': 'failure',
                'message': f"City with name: '{data['name']}' already exists",
            }

            return response

    # TODO: By name and country code or ID
    def get_city_by_name(self, name):
        return self.db.cities.find_one({"name": name})

    def get_city_by_city_id(self, city_id):
        return self.db.cities.find_one({"city_id": city_id})

    def get_all(self):

        # just to have some feedback
        for city in self.db.cities.find():
            pprint.pprint(city)

        return list(self.db.cities.find())

    # def update_all(self, data):

    def remove_database(self):

        return self.db.cities.drop()


