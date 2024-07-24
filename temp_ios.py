import requests
from rich import print
from dataclasses import dataclass

country_codes = ['US']

APPS_DATA = {
  'ELVIE' : '1349263624',
  'WILLOW_G0' : '1579004074',
  'WILLOW_3' : '1489872855',
  'TOMMEE_TIPPEE' : '1522124003',
  'MEDELA' : '909275386',
  'LANSINOH' : '1480550011'
}

APP_ID = APPS_DATA['WILLOW_G0']

reviews_list = []

@dataclass
class Review:
  date: str
  country: str
  user_rating: int
  title: str
  body: str
  vote_sum: int
  vote_count: int
  app_version: str

def parse_reviews_data(reviews_data):
  parsed_reviews = []
  try: 
    for review_item in reviews_data:
      review = Review (
        date = review_item['updated']['label'].split("T")[0],
        country =  review_item['author']['uri']['label'].split('/')[3],
        app_version = review_item['im:version']['label'],       
        user_rating = int(review_item['im:rating']['label']),
        title = review_item['title']['label'],
        body =  review_item['content']['label'],
        vote_sum = int(review_item['im:voteSum']['label']),
        vote_count = int(review_item['im:voteCount']['label'])  
      )
      parsed_reviews.append(review)
    return(parsed_reviews)
  except Exception as e:
    print(f"An error occurred: {e}")

def save_to_excel(df):
  df.to_excel('ios-elvie-reviews.xlsx', index = False)

def get_reviews(country_code,app_id):
  print(f'Getting reviews for countries: {country_code}')
  r = requests.get(f'https://itunes.apple.com/{country_code}/rss/customerreviews/page={1}/id={app_id}/sortby=mostrecent/json?urlDesc=/customerreviews/id={app_id}/sortby=mostrecent/json').json()
  try:
      reviews_response = r['feed']
      attributes_list = reviews_response['link']
      # return the item  (first item) that results of iterating over each item (second item) of the attributes list if the attributes rel is last
      last_attribute= next(item for item in attributes_list if item['attributes']['rel'] == 'last')
      last_url = last_attribute['attributes']['href']
      last_page = int(last_url.split('page=')[1].split('/')[0])
      for page_num in range(1, last_page + 1):
        r = requests.get(f'https://itunes.apple.com/{country_code}/rss/customerreviews/page={page_num}/id={app_id}/sortby=mostrecent/json?urlDesc=/customerreviews/id={app_id}/sortby=mostrecent/json').json()
        page_reviews = r['feed']['entry']
        data_with_country = [{**entry, 'country': country_code} for entry in page_reviews]
        reviews_list.extend(data_with_country)
      
  except Exception as e:
      print(f'No reviews for country {country_code}: {e}')
      return

def main():
  for country in country_codes:
    get_reviews(country, APP_ID)
  formatted_reviews = parse_reviews_data(reviews_list)
  print(formatted_reviews)

main()
