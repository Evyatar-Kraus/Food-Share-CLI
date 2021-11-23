from shared_food import SharedFood
from faker import Faker

fake = Faker()

food_names_list = [
    'danish', 'cheesecake', 'sugar',
    'Lollipop', 'wafer', 'Gummies',
    'sesame', 'beans',
    'pie', 'bar', 'Ice', 'oat']

first_name_list = ['Dani', 'Daniel', 'Alice', 'Johnny', 'Yogev', 'Sarah']
last_name_list = ['Coh', 'Daniel', 'Alice', 'Johnny', 'Yogev', 'Sarah']
# building_number = range(0,21)
# street_name = []
# city = []
# country = []
fake_address  = "herzl 8 tel aviv israel"

def faker_shared_food_generate(type=None, faker_mode=False):
    shared_food_attributes = {
        'food_title': fake.word(ext_word_list=food_names_list).capitalize(),
        'food_text': ' '.join(fake.sentence(ext_word_list=food_names_list).split(' ')[0:4]),
        # 'food_text':"'Cheesecake with a sprinkle of sugar'",
        # 'address': fake_address or f"{fake.street_address()}, {fake.city()}, {fake.country()}",
        'country':'israel',
        'city':'tel aviv',
        'street_name':'david ben gurion',
        'building_number':'8',
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'contact_phone': fake.phone_number(),
    }

    faked_attrs = {
            'user_id': fake.pyint(min_value=1, max_value=500),
            'created_at': fake.date(),
            'updated_at': fake.date(),
            'published': fake.boolean(),
    }

    if faker_mode:
        shared_food_attributes.update(faked_attrs)

    return shared_food_attributes.get(type) or faked_attrs.get(type) if type else shared_food_attributes


# print(faker_user_generate())
# print(faker_user_generate('user_id'))


# new_food_share = SharedFood(faker_shared_food_generate())
# print(vars(new_food_share))
# print(new_food_share.user_id)

# print(SharedFood.get_by_id(3))
SharedFood(faker_shared_food_generate())
