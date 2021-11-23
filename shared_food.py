#   shared food has attributes
#   food name
#   food address - calculate coordinates
#   sharedFood can:
#   save - to db
#   publish - change attribute published to true
#   unpublish - change attribute published to false
#   get_address - get shared food address
#   update - change details - name or address
#   remove - delete itself

import psycopg2
from psycopg2 import sql
from utils import run_query, get_distance
from datetime import datetime
import itertools
from location_api import address_to_coords

_GIVEN_ATTRIBUTES = ['first_name', 'last_name', 'food_title',
                    'food_text', 'contact_phone', 'country','city','street_name','building_number'] #given when calling the class
_SELF_GENERATED_ATTRIBUTES = ['updated_at','created_at','published','lon','lat'] #generated in __init__
pkey = 'shared_food_id'

class SharedFood:
    #class attributes
    format_code = '%Y/%m/%d'
    _TABLE_NAME = 'shared_foods'
    #column list for row that represent the invoked instace in the database table
    column_list = list(itertools.chain(_GIVEN_ATTRIBUTES,_SELF_GENERATED_ATTRIBUTES))
    _pkey = pkey
    def __init__(self, kwargs):
        # given when calling the class
        for keyword, value in kwargs.items():
            if keyword in _GIVEN_ATTRIBUTES or keyword in _SELF_GENERATED_ATTRIBUTES or  keyword == pkey:
                setattr(self, keyword, value)
            else:
                raise ValueError(
                    "Unknown keyword argument: {!r}".format(keyword))

        self.created_at = datetime.strftime(
            datetime.now(), self.format_code)
        self.updated_at = datetime.strftime(
            datetime.now(), self.format_code)

        if not hasattr(self,'lat'):
            try:
                coordinates = address_to_coords(self.building_number,self.street_name,self.city,self.country)
                self.lat = coordinates['lat']
                self.lon = coordinates['lon']
            except:
                print("Error getting address coordinates - coordinates will not be saved")

        self.published = str(True)
        if not hasattr(self,'shared_food_id'):
            self.shared_food_id = self.save()

    def save(self):
        print("save - insert to db here")
        column_list = self.column_list
        value_list = [getattr(self,key) for key in self.column_list]
        query = sql.SQL("insert into {} ({col_names}) values ({values}) returning shared_food_id").format(
            sql.Identifier(self._TABLE_NAME),
            col_names = sql.SQL(', ').join(sql.Identifier(n) for n in column_list),
             values = sql.SQL(', ').join(sql.Literal(n) for n in value_list )
            )
        result_tuple = run_query(query,mode='wr1')
        shared_food_id = result_tuple[0]
        print(f"id of created shared food: {shared_food_id}")
        return shared_food_id

    def distance_by_km_from_address(self,num,st,city,country):
        address_coords = address_to_coords(num,st,city,country)
        address_lat = float(address_coords['lat'])
        address_lon = float(address_coords['lon'])
        distance = get_distance(address_lat,address_lon,self.lat,self.lon )
        return distance

    @classmethod
    def get_by_id(cls,id):
        columns = cls.column_list.copy()
        columns.insert(0,'shared_food_id')
        query = sql.SQL("select {} from {} where {} = {}").format(
            sql.SQL(', ').join(sql.Identifier(n) for n in columns),
            sql.Identifier(cls._TABLE_NAME),
            sql.Identifier(cls._pkey),
            sql.Literal(id)
        )
        result = run_query(query,mode="r1")
        zipped = list(zip(columns,result))
        attr_dict = dict(zipped)
        return SharedFood(attr_dict)

    @classmethod
    def all(cls):
        columns = cls.column_list.copy()
        columns.insert(0,'shared_food_id')
        query = sql.SQL("select {} from {};").format(
            sql.SQL(', ').join(sql.Identifier(n) for n in columns),
            sql.Identifier(cls._TABLE_NAME),
            )
        results = run_query(query,mode="ra")
        all_foods = []
        for result in results:
            food = SharedFood(dict(list(zip(columns,result))))
            all_foods.append(food)
        return all_foods

    def delete(self):
        print("trying to delete")
        query = sql.SQL("delete from {} where {} = {} returning shared_food_id,food_title") .format(
            sql.Identifier(self._TABLE_NAME),
            sql.Identifier('shared_food_id'),
            sql.Literal(self.shared_food_id))
        result = run_query(query, mode="wr1")
        print(f"deleted food #{result[0]}: {result[1]}")

    def __str__(self):
                return f'''\n#{self.shared_food_id}: {self.food_title}
description: {self.food_text}
name: {self.first_name} {self.last_name}
contact phone: {self.contact_phone}
city: {self.city}'''

    def __repr__(self):
        return f'<SharedFood id:#{self.shared_food_id}: {self.food_title}>'
