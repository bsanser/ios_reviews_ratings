import requests
from rich import print
from datetime import datetime


countries=["DZ", "AO", "AI",
"AR", "AM", "AU", "AT", "AZ", "BH", "BB", "BY", "BE", "BZ", "BM", "BO","BW", "BR", "VG", "BN", "BG", "CA","KY", "CL", "CN", "CO", "CR", "HR", "CY", "CZ", "DK", "DM", "EC", "EG",
"SV", "EE", "FI","FR", "DE", "GH","GB", "GR", "GD","GT", "GY", "HN","HK", "HU", "IS","IN", "ID", "IE","IL", "IT", "JM", "JP", "JO", "KE", "KW", "LV", "LB","LT", "LU", "MO", "MG", "MY", 
"ML","MT", "MU", "MX","MS", "NP", "NL", "NZ", "NI", "NE","NG", "NO", "OM","PK", "PA", "PY","PE", "PH", "PL","PT", "QA", "MK", "RO", "RU", "SA","SN", "SG", "SK","SI", "ZA", "KR", "ES", 
"LK", "SR","SE", "CH", "TW","TZ", "TH", "TN","TR", "UG", "UA","AE", "US", "UY","UZ", "VE", "VN","YE"]

countries_with_ratings = []

def get_countries_with_ratings(data):
    return [entry['country'] for entry in data]

def calculate_total_number_of_ratings(data):
    return sum(entry['ratings_count'] for entry in data)

    
def get_country_ratings_count(app_id, country):
 try:
  r = requests.get(f'http://itunes.apple.com/lookup?id={app_id}&country={country}').json() 
  ratings_count = r['results'][0]['userRatingCount']
  if ratings_count > 0:
    countries_with_ratings.append({"country": country, "ratings_count": ratings_count})
 except Exception as e:
  print(f'Country {country} raised the following exception: {e}')

def get_app_info(app_id, total_ratings_count):
  r = requests.get(f'http://itunes.apple.com/lookup?id={app_id}').json() 
  response= r['results'][0]
  formatted_date = datetime.fromisoformat(response['currentVersionReleaseDate'][:-1]).strftime('%Y-%m-%d')
  app_info = {
    "latest_release_date" : formatted_date,
    "latest_release_version" : response['version'],
    "latest_release_notes" : response['releaseNotes'],
    "total_ratings_count" : total_ratings_count
  }
  return app_info


def get_total_ratings_count(countries_with_ratings_list):
  total_ratings_count = calculate_total_number_of_ratings(countries_with_ratings_list)
  return total_ratings_count



def get_countries_with_ratings_list(app_id):
  print(f'Start time: {datetime.now()}')
  print('Getting countries with ratings list')
  for country in countries:
    get_country_ratings_count(app_id, country)
  countries_with_ratings_list = get_countries_with_ratings(countries_with_ratings)
  return countries_with_ratings_list


