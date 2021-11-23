import requests
# example_location_api_url = 'https://nominatim.openstreetmap.org/search.php?q=herzl+8+tel+aviv+israel&format=jsonv2'
# exmaple = https://nominatim.openstreetmap.org/search.php?q=moshe+sharet+8+tel+aviv+israel&format=jsonv2
# strucuted_example =https://nominatim.openstreetmap.org/search.php?street=8+%2F+eilat&city=tel+aviv+&country=israel&format=jsonv2
location_api_url = 'https://nominatim.openstreetmap.org/search.php'


def address_to_coords(num,st,city,country):
    try:
        st = '+'.join(st.split(' '))
        city = '+'.join(city.split(' '))
        country = '+'.join(country.split(' '))
        address = f"street={num}+%2F+{st}&city={city}+&country={country}"
        url = f'{location_api_url}?{address}&format=jsonv2'
        response = requests.get(url)
        coords = {'lat':response.json()[0]['lat'],'lon':response.json()[0]['lon']}
        return coords;
    except:
        raise Exception("error getting coordinates from address")

# print(address_to_coords(8,"herzl","tel aviv","israel"))