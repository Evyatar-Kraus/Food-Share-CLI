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

from logging import PlaceHolder
import psycopg2
from psycopg2 import sql
from utils import run_query, get_distance
from datetime import datetime
from pprint import pprint
import itertools
from location_api import address_to_coords



#table create script
# CREATE TABLE shared_foods
#  (
#      shared_food_id serial primary key,
#      food_title varchar(100) NOT NULL,
#      food_text text NOT NULL,
#      first_name varchar(50) NOT NULL,
#      last_name varchar(50) NOT NULL,
#      user_id INTEGER NOT NULL,
#      address point NOT NULL, -- as coordinates
#      contact_phone varchar(20) NOT NULL
#      created_at DATE NOT NULL DEFAULT CURRENT_DATE,
#      updated_at DATE NOT NULL DEFAULT CURRENT_DATE,
#      published BOOLEAN NOT NULL DEFAULT FALSE ,
#      FOREIGN key(user_id) references user(user_id)
# );

__TABLE_NAME ='shared_foods'

_GIVEN_ATTRIBUTES = ['first_name', 'last_name', 'food_title',
                    'food_text', 'contact_phone', 'address'] #given when calling the class
_SELF_GENERATED_ATTRIBUTES = ['updated_at','created_at','published','lon','lat'] #generated in __init__
_DB_GENERATED_ATTRIBUTES = ['shared_food_id']

class SharedFood:
    #class attributes
    format_code = '%Y/%m/%d'
    _TABLE_NAME = 'shared_foods'
    #column list for row that represent the invoked instace in the database table
    column_list = list(itertools.chain(_GIVEN_ATTRIBUTES,_SELF_GENERATED_ATTRIBUTES))

    def __init__(self, kwargs):
        # given when calling the class
        for keyword, value in kwargs.items():
            if keyword in _GIVEN_ATTRIBUTES:
                setattr(self, keyword, value)
            else:
                raise ValueError(
                    "Unknown keyword argument: {!r}".format(keyword))

        self.lat = None
        self.lon = None
        self.coordinates = {'lat':None,'lon':None}

        try:
            self.coordinates = address_to_coords(self.address)
            self.lat = self.coordinates['lat']
            self.lon = self.coordinates['lon']
        except:
            print("Error getting address coordinates - coordinates will not be saved")

        self.created_at = datetime.strftime(
            datetime.now(), self.format_code)
        self.updated_at = datetime.strftime(
            datetime.now(), self.format_code)
        self.published = str(False)
        shared_food_id = self.save()

    # def modify(self, **kwargs):
    #     #change details based on a passed dictionary
    #     pass

    def save(self):
        print("save - insert to db here")

        column_list = self.column_list
        value_list = [getattr(self,key) for key in self.column_list]
        pprint(column_list)
        pprint(value_list)
        col_names = sql.SQL(', ').join(sql.Identifier(n) for n in column_list )
        values = sql.SQL(', ').join(sql.Literal(n) for n in value_list )

        # query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING RETURNING shared_food_id").format(
            # table_name =sql.Identifier(self._TABLE_NAME),  # table name
            # col_names = col_names,
            # values = values
        # )

        # query = f"INSERT INTO {self._TABLE_NAME} ({ ', '.join(column_list) }) VALUES ({', '.join(value_list)}) \
        #     ON CONFLICT DO NOTHING RETURNING shared_food_id;"
        print()
        print(len(column_list))
        print(len(value_list))
        query = sql.SQL("insert into {} ({col_names}) values ({values})").format(
            sql.Identifier(self._TABLE_NAME),
            col_names = sql.SQL(', ').join(sql.Identifier(n) for n in column_list),
             values = sql.SQL(', ').join(sql.Literal(n) for n in value_list )
            )
        print(query)
        result = run_query(query,mode='w')
        print(result)


    def publish(self):
        # change this one's published status to True
        try:
            query =  sql.SQL("update {} set published = true where shared_food_id = %s;") .format(
            sql.Identifier(__TABLE_NAME)),  [self.shared_food_id]
            run_query(query)
            self.published = True
        except:
            print("Error publishing this food")
            pass

    def unpublish(self):
        # change this one's published status to False
        try:
            query =  sql.SQL("update {} set published = false where shared_food_id = %s;") .format(
            sql.Identifier(__TABLE_NAME)),  [self.shared_food_id]
            run_query(query)
            self.published = False
        except:
            print("Error unpublishing this food")
            pass

    def distance_by_km_from_address(self,address):
        # get distance from user - or from coordinates
        distance = get_distance(address_to_coords(address))
        # SELECT ST_DistanceSphere(ST_MakePoint(103.776047, 1.292149),ST_MakePoint(103.77607, 1.292212));
        return distance
        pass

    def to_json(self):
        # print('to_json')
        data = vars(self)
        data['created_at'] = datetime.strftime(
            data['created_at'], self.format_code)
        data['updated_at'] = datetime.strftime(
            data['updated_at'], self.format_code)
        # print(data)
        # data = {
        #     'first_name':self.first_name,
        #     'last_name':self.last_name,
        #     'food_name':self.food_name,
        #     'food_text':self.food_text,
        #     'food_address':self.food_address,
        #     'published':self.published,
        #     'contact_phone':self.contact_phone,
        #     'created_at':self.created_at,
        #     'updated_at':self.updated_at
        # }
        return data

    @classmethod
    def from_json(cls):
        pass

    def delete(self, id):
        # remove this sharing from the database
        query = f'DELETE from {__TABLE_NAME} where shared_food_id = {id};'
        query = sql.SQL("insert into {} values (%s, %s)") .format(
            sql.Identifier(__TABLE_NAME)),  [self.created_date]
        print("deleted")
        pass

    def date_str(self):
        return self.date.strftime(self.format_code)

    def __str__(self):
        pass
        # return f'{self.date_str()}'

    def __repr__(self):
        pass
        # return self.__str__()
