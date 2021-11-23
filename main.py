from menu import  show_user_menu, show_foods, add_food, remove_food, get_specific_food, show_start_greeting



def main():
    show_start_greeting()
    country = input("Please enter country:\n")
    city = input("City:\n")
    street_name = input("Street Name:\n")
    street_number = input("Building Number:\n")
    while(user_input := show_user_menu()):
        if user_input == 's':
            show_foods(street_number,street_name,city,country)
        elif user_input == 'd':
            remove_food()
        elif user_input == 'a':
            add_food()
        elif user_input == 'g':
            get_specific_food()
        elif user_input == 'x':
            print("Good Bye!")
            break


if __name__ == '__main__':
    main()