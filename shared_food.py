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

from psycopg2 import sql
# from utils import run_query
from datetime import datetime

__TABLE_NAME = 'shared_foods'

class SharedFood:
    def __init__(self,**kwargs) -> None:
        #given when calling the class
        _VALID_KEYWORDS = {'user_id','food_title','food_text','contact_phone','address'}
        for keyword, value in kwargs.items():
            if keyword in self._VALID_KEYWORDS:
                setattr(self, keyword, value)
            else:
                raise ValueError(
                    "Unknown keyword argument: {!r}".format(keyword))
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.published = False
        self.save()

    def modify(self, **kwargs):
        #change details based on a passed dictionary
        pass

    def save(self):
        #insert to database here
        pass

    def publish(self):
        #change this one's published status to True
        pass

    def unpublish(self):
        #change this one's published status to False
        pass

    def distance_from(self,user_id=None,coordinates={}):
        #get distance from user - or from coordinates
        pass

    def to_json(self):
        data = {
            'first_name':self.first_name,
            'last_name':self.last_name,
            'food_name':self.food_name,
            'food_text':self.food_text,
            'food_address':self.food_address,
            'published':self.published,
            'contact_phone':self.contact_phone,
            'created_date':self.created_date,
            'updated_date':self.updated_date
        }
        return data

    def delete(self):
        #remove this sharing from the database
        pass

    def save(self):
        # query = f"INSERT INTO student (first_name, last_name, class_id) VALUES \
        # ('{self.first_name}', '{self.last_name}', '{self.classroom.id}')"
        # query = sql.SQL("insert into {} values (%s, %s)") .format(sql.Identifier('my_table')),  [10, 20]
        # run_query(query)
        pass