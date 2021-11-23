# hackaton-2
Food Share - preventing food waste!
Command line application to share food you don't want with others (distance based)
Alternatively - you can see which foods other want to give away!

This application uses open street api for getting the coordinates from an address
and the h3 package by uber to measure the distance between the user's address to the other users sharings.

# instructions
take .env.example file - change it to .env
put it one folder above root of this application and fill the details there
to allow connection to the db

script to create the table
```
table create script
 CREATE TABLE shared_foods
  (
    shared_food_id NOT NULL serial primary key,
    food_title varchar(100) NOT NULL,
    food_text text NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    country varchar(50),
    city varchar(50),
    street_name varchar(50),
    building_number varchar(10),
    contact_phone varchar(20) NOT NULL,
    lat double precision,
    lon double precision,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    updated_at DATE NOT NULL DEFAULT CURRENT_DATE,
    published BOOLEAN NOT NULL DEFAULT TRUE ,
);