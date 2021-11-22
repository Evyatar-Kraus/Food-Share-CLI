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


        self.published = str(False)
        if not hasattr(self,'shared_food_id'):
            self.shared_food_id = self.save()

    # def modify(self, **kwargs):
    #     #change details based on a passed dictionary
    #     pass

    def save(self):
        print("save - insert to db here")

        column_list = self.column_list
        value_list = [getattr(self,key) for key in self.column_list]
        # pprint(column_list)
        # pprint(value_list)

        # col_names = sql.SQL(', ').join(sql.Identifier(n) for n in column_list )
        # values = sql.SQL(', ').join(sql.Literal(n) for n in value_list )

        # query = f"INSERT INTO {self._TABLE_NAME} ({ ', '.join(column_list) }) VALUES ({', '.join(value_list)}) \
        #     ON CONFLICT DO NOTHING RETURNING shared_food_id;"

        # print()
        # print(len(column_list))
        # print(len(value_list))

        query = sql.SQL("insert into {} ({col_names}) values ({values}) returning shared_food_id").format(
            sql.Identifier(self._TABLE_NAME),
            col_names = sql.SQL(', ').join(sql.Identifier(n) for n in column_list),
             values = sql.SQL(', ').join(sql.Literal(n) for n in value_list )
            )

        # print(query)
        result_tuple = run_query(query,mode='wr1')
        shared_food_id = result_tuple[0]
        print(f"id of created shared food: {shared_food_id}")
        return shared_food_id


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

    def distance_by_km_from_address(self,num,st,city,country):
        # get distance from user - or from coordinates
        address_coords = address_to_coords(num,st,city,country)
        address_lat = float(address_coords['lat'])
        address_lon = float(address_coords['lon'])
        # print(address_to_coords)
        print("measure distance")
        print(self.lat,self.lon)
        print(address_lat,address_lon)
        distance = get_distance(address_lat,address_lon,self.lat,self.lon )
        print(distance)
        return distance
        # return f"{distance:.2f}km"


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
        print("\nzipped")
        print(zipped)
        print("\ndict")
        attr_dict = dict(zipped)
        print(attr_dict)
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
        # results = [dict(list(zip(columns,result)) for result in results)]
        # print(results)
        all_foods = []
        for result in results:
            food = SharedFood(dict(list(zip(columns,result))))
            print(food)
            all_foods.append(food)
            # print(all_foods)
        print('\n\n\n')
        print(all_foods,sep="\n")
        # print(all_foods)
        # for result in results:
            # print(dict(list(zip(columns,result))))
            # print("\n\n")
        # results = list(map(lambda res: MenuItem(res[0],res[1]),results))
        return all_foods

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
                return f'''\n#{self.shared_food_id}: {self.food_title}
    description: {self.food_text}
    name: {self.first_name} {self.last_name}
    contact phone: {self.contact_phone}
    city: {self.city}'''



    def __repr__(self):
        return f'<SharedFood id:#{self.shared_food_id}: {self.food_title}>'
