#Import packages
import googlemaps
import pandas as pd

# Import locations
locations = pd.read_csv('Major Cities.csv')

# Google API Instance
gmaps = googlemaps.Client(key='AIzaSyAtgajuDmi4xjv1frQIvLfawsA5XGMPDxo')

# Gather all DMV Locations
DMV_List = pd.DataFrame(columns = ['name','place_id','types'])

for i in locations.Locations:
    response = gmaps.places(query='DMV in '+i)

    if len(response['results']) > 0:
        res_df = pd.DataFrame(columns=['name','place_id','types'])

        for biz in response['results']:
            res_df.loc[len(res_df)] = [biz['name'], biz['place_id'], biz['types']]

        DMV_List = DMV_List.append(res_df)
        print(i,": ",len(res_df))
    else:
        print(i,": ",'0')

# Gather all reviews from locations
ID_list = DMV_List.place_id
Review_List = pd.DataFrame(columns = ['text','rating'])

for i in ID_list:
    response = gmaps.place(place_id=i)

    try:
        if len(response['result']['reviews']) > 0:
            res_df = pd.DataFrame(columns=['text','rating'])

            for rev in response['result']['reviews']:
                res_df.loc[len(res_df)] = [rev['text'], rev['rating']]

            Review_List = Review_List.append(res_df)
            print(i,": ",len(res_df))
    except:
        print(i,": ",'0')

Review_List.to_csv('Google_Reviews.csv')

