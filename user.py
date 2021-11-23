
# from utils import run_query
# from shared_food import SharedFood

# # User has attributes
# # first_name, last_name, user_id, address, user_name -?, phone
# #
# # user can:
# # publish food to share
# # see shared food

# class User:
#     def __init__(self,user_id,**kwargs):
#         format_code = '%Y/%m/%d'

#         #All the attributes for a new user are here in _VALID_KEYWORDS
#         _VALID_KEYWORDS = {'first_name','last_name','user_name', 'email', 'address'}
#         for keyword, value in kwargs.items():
#             if keyword in self._VALID_KEYWORDS:
#                 setattr(self, keyword, value)
#             else:
#                 raise ValueError(
#                     "Unknown keyword argument: {!r}".format(keyword))
#         if not user_id:
#             self.save()

#     #TODO add options like time to shared food so posting will be removed after x time (trigger)
#     def add_shared_food(self):
#         new_food = SharedFood()
#         new_food.save_shared_food()

#     def to_json(self,format_code):
#         data = {
#             'first_name':self.first_name,
#             'last_name': self.last_name,
#             'address': self.address
#             # 'time_created': time_created.strftime(format_code)
#             # 'time_updated': time_updated.strftime(format_code)
#             # 'shared_food': get_user_shared_foods_json(self.user_id)
#             }
#         return data


#     def remove(self):
#         pass

#     def update(self):
#         pass

#     #TODO change to safe query parameters
#     def save(self):
#         query = f"INSERT INTO student (first_name, last_name, class_id) VALUES ('{self.first_name}', '{self.last_name}', '{self.classroom.id}')"
#         run_query(query)
