from datetime import datetime
import requests
from rich import print
import pandas as pd
from helpers import get_countries_with_ratings_list, parse_reviews_data
# from save_to_gsheets import save_to_gsheets, update_gsheets
from constants import APP_IDS
import logging

logging.basicConfig(filename='cron.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

APP_ID = APP_IDS.get('ELVIE', 'App not found')


country_codes = get_countries_with_ratings_list(APP_ID)


app_name = next(key for key, value in APP_IDS.items() if value == APP_ID).lower()

reviews_list = []



def save_to_excel(df):
 df.to_excel('ios-elvie-reviews.xlsx', index = False)

def get_reviews(country_code,app_id):
  print(f'Getting reviews for countries: {country_code}')
  response = requests.get(f'https://itunes.apple.com/{country_code}/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json?urlDesc=/customerreviews/id={app_id}/sortby=mostrecent/json').json()
  if 'feed' in response:  
    reviews_response = response['feed']
    attributes_list = reviews_response['link']
     # return the item  (first item) that results of iterating over each item (second item) of the attributes list if the attributes rel is last
    last_attribute= next(item for item in attributes_list if item['attributes']['rel'] == 'last')
    last_url = last_attribute['attributes']['href']
    if last_url != "":
      last_page = int(last_url.split('page=')[1].split('/')[0])
      for page_num in range(1, last_page + 1):
        try: 
          r = requests.get(f'https://itunes.apple.com/{country_code}/rss/customerreviews/page={page_num}/id={app_id}/sortby=mostrecent/json?urlDesc=/customerreviews/id={app_id}/sortby=mostrecent/json').json()
          page_reviews = r['feed']['entry']
          if isinstance(page_reviews, dict):
              page_reviews['country'] = country_code
              reviews_list.append(page_reviews)
          elif isinstance(page_reviews, list):
            # for review in page_reviews:
            #     review['country'] = country_code
            #     reviews_list.extend(page_reviews)
            data_with_country = [{**entry, 'country': country_code} for entry in page_reviews]
            reviews_list.extend(data_with_country)
        except Exception as e:
          print(f'exception for country: {country_code}, exception: {e}')

def main():
  for country in country_codes:
    get_reviews(country, APP_ID)
  print(f'Found {len(reviews_list)} reviews in total')
  print(f'End time: {datetime.now().strftime("%H:%M:%S")}')
  formatted_reviews = parse_reviews_data(reviews_list)
  df = pd.DataFrame(formatted_reviews)
  df.head()
  # sorted_by_most_recent_df = df.sort_values(by='date', ascending=False)
  # sorted_by_most_recent_df.to_excel(f'ios_{app_name}_reviews.xlsx')
  # sorted_by_most_recent_df.to_csv(f'ios_{app_name}_reviews.csv', index=False)
  
  # print('Updating spreadsheet')
  # update_gsheets(sorted_by_most_recent_df)
  # save_to_gsheets(sorted_by_most_recent_df)
  # save_to_excel(sorted_by_most_recent_df)

main()

