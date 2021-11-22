from location_api import address_to_coords
from shared_food import SharedFood
from shared_food import _GIVEN_ATTRIBUTES
from utils import get_distance

def show_user_menu():
    #show user menu
    user_input = input('''
    MENU
    (s) Search foods near you
    (a) Add a food
    (d) Delete a food
    (v) View all the foods
    (x) Exit
    ''')
    return user_input


def load_manager(*args):
    return SharedFood(*args)


def add_food():
    print("Adding a new item to the menu:\n")
    shared_food_attributes = {}
    for att in _GIVEN_ATTRIBUTES:
        shared_food_attributes[att] = input(f"What is the {att}?\n")
    new_food_to_add = load_manager(shared_food_attributes)
    try:
        # new_item_to_add.save()
        print("item was added successfully.\n")
    except:
        print("Error adding item.")


def remove_food():
    item_to_remove_input = input("What item do you want to remove?\n")
    try:
        menu_item = SharedFood.get_by_name(item_to_remove_input)
        print(menu_item)
        menu_item.delete()
        print("Item deleted successfully")
    except:
        print("Error - item was not deleted")


#TODO need to sort these by location
#so it will show the closest first etc...
def show_foods(num,st,city,country):
    #show all items in menu
    print(f"{num} {st} {city} {country}")
    foods = SharedFood.all()
    distances = {}
    for food in foods:
        distances[food.shared_food_id] = food.distance_by_km_from_address(num,st,city,country)
    for item in foods:
        print(item.city)
        print(item.street_name)
        print(f"""{item}
        distance: {distances[item.shared_food_id]:.2f}km
        """)
