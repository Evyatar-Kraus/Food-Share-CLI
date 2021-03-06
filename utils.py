import psycopg2
import os

from dotenv import dotenv_values
import h3


def get_env_db_info_dict():
    config = dotenv_values(os.path.join(os.path.dirname(__file__), '../.env'))
    return config
pg_env_details = get_env_db_info_dict()
pg_details = {'host': pg_env_details.get('db_host'), 'user':pg_env_details.get('db_user'),
 'password': pg_env_details.get('db_pass'), 'dbname':pg_env_details.get('db_name')}

def run_query(query, mode='w'):
    connection = psycopg2.connect(**pg_details)
    cursor = connection.cursor()
    cursor.execute(query)
    if 'ra' in mode:
        results = cursor.fetchall()
    if 'r1' in mode:
        results = cursor.fetchone()
    connection.commit()
    connection.close()
    if 'r' in mode :
        return results

def get_distance(lat1, lng1, lat2, lng2):
    coords_1 = (lat1, lng1)
    coords_2 = (lat2, lng2)
    distance = h3.point_dist(coords_1, coords_2, unit='km') # to get distance in km
    return distance