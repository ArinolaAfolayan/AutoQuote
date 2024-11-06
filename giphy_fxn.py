# test using giphy api
# https://developers.giphy.com/docs/resource/#code-examples

import requests
import json

API_KEY = 'XkeQMprRuhwjR2IpISzEsrOUDH9CDksZ'
url = 'https://api.giphy.com/v1/gifs/search'

def giphy_call(query):
    p = {
        'api_key': API_KEY,
        'q': query,
        'limit': 1,
    }
    p_cat = {
        'api_key': API_KEY,
        'q': 'cat',
        'limit': 1,
    }

    # store content that we get from our page.
    response = requests.get(url, params=p)

    if response.status_code == 200:
        # successful
        response_data = response.json()
        # display the url for the original gif
        gif_url = response_data['data'][0]['images']['fixed_height']['url']
        print('\n' + gif_url + '\n')
        # print(json.dumps(response_data, sort_keys=True, indent=4))
        print("Retrival of GIF was successful.")
    else:
        print("Retrieval of GIF failed.")
        response_cat = requests.get(url, params=p_cat)
        if response_cat.status_code == 200:
            response_cat_data = response_cat.json()
            gif_url = response_cat_data['data'][0]['images']['fixed_height']['url']

    return gif_url


# test
# giphy_call('cat')