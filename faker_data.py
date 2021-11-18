from faker import Faker
fake = Faker()

food_names_list = [
'danish','cheesecake','sugar',
'Lollipop','wafer','Gummies',
'sesame','Jelly','beans',
'pie','bar','Ice','oat' ]

first_name_list = ['Dani','Daniel','Alice','Johnny','Yogev','Sarah']
last_name_list = ['Coh','Daniel','Alice','Johnny','Yogev','Sarah']


def faker_user_generate(type=None):
    types = {
        'user_id':fake.pyint(min_value=1,max_value=500),
        'food_title':fake.word(ext_word_list=food_names_list).capitalize(),
        'food_text':' '.join(fake.sentence(ext_word_list=food_names_list).split(' ')[0:4]*4),
        'address': f"{fake.street_address()}, {fake.city()}, {fake.country()}",
        # 'first_name':fake.first_name(),
        # 'last_name':fake.last_name(),
        'created_date':fake.date(),
        'updated_date':fake.date(),
        'contact_phone':fake.phone_number(),
        'published':fake.boolean()
    }

    return types.get(type) if type else types


print(faker_user_generate())
print(faker_user_generate('user_id'))
print(faker_user_generate('food_title'))
# print(faker_user_generate('food_text'))
# print(faker_user_generate('address'))
# print(faker_user_generate('first_name'))
# print(faker_user_generate('last_name'))
# print(faker_user_generate('created_date'))
# print(faker_user_generate('updated_date'))
# print(faker_user_generate('published'))
# print(faker_user_generate('contact_phone'))
