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
    (g) Show specific food
    (x) Exit
    ''')
    return user_input

def add_food():
    print("Adding a new food:\n")
    shared_food_attributes = {}
    for att in _GIVEN_ATTRIBUTES:
        shared_food_attributes[att] = input(f"What is the {att}?\n")
    try:
        new_food_to_add = SharedFood(shared_food_attributes)
        print(new_food_to_add.get_created_at())
        print("item was added successfully.\n")
    except:
        print("Error adding item.")


def remove_food():
    food_to_remove_id_input = input("What item do you want to remove? please enter the id:\n")
    try:
        food = SharedFood.get_by_id(int(food_to_remove_id_input))
        food.delete()
        print("Item deleted successfully")
    except:
        print("Error - item was not deleted")


#TODO need to sort these by location
#so it will show the closest first etc...
def show_foods(num,st,city,country):
    foods = SharedFood.all()
    distances = {}
    for food in foods:
        distances[food.shared_food_id] = food.distance_by_km_from_address(num,st,city,country)
    for item in foods:
        print(f"""{item}
distance: {distances[item.shared_food_id]:.2f}km
        """)

def get_specific_food():
        food_id = input("what is the food id?\n")
        food = None
        while not food:
            try:
                food = SharedFood.get_by_id(int(food_id))
                print(food)
                print(food.get_created_at())
            except:
                print("error - maybe check if the id is valid?")
            finally:
                continue

def show_start_greeting():
    print("Welcome to food share!")
    print("""Here you can share food you don't want with your neighbors!
Or get something tasty to eat... and avoid waste all together!
\n""")