#Import packages
from yelpapi import YelpAPI
import pandas as pd

# Import locations
locations = pd.read_csv('Major Cities.csv')

# Set up Yelp API
client_id = 'DVi_4btNemHREJJcT-JCKA'
api_key = 'nmCmLYxw_ewkTiftE-J5DaZyJMTr8ZpqJ7FbzWNCu-dMJ-lEgVstKhba5mseN_1wz0MR8i25BBWCDq-QykHardSzGhy4ZqWUc4zKidmqsxyug8hWi82lCAMGXhmQYXYx'
yelp_api = YelpAPI(api_key)

# Gather all DMV Locations
DMV_List = pd.DataFrame(columns=['id','name','url', 'review_count','categories', 'DMV_Check'])

for i in locations.Locations:
    response = yelp_api.search_query(term = 'DMV',
                                     location = i,
                                     limit = 50)

    if response['total'] > 0:
        cols = list(response['businesses'][0].keys())
        res_df = pd.DataFrame(columns=cols)

        for biz in response['businesses']:
            res_df = res_df.append(biz, ignore_index=True)

        res_df = res_df[['id','name','url', 'review_count','categories']]

        DMV_Check = []

        for j in res_df.categories:
            DMV_Check.append(j[0]['alias'] == 'departmentsofmotorvehicles')

        res_df['DMV_Check'] = DMV_Check
        res_df = data[data.DMV_Check == True]

        DMV_List = DMV_List.append(res_df)
        print(i,": ",len(res_df))
    else:
        print(i,": ",'0')


# Drop duplicates
DMV_List = DMV_List.drop_duplicates(subset = ['id'])

# Get reviews for each location
Review_List = pd.DataFrame(columns=['id', 'text', 'rating'])

for i in DMV_List.id:
    response = yelp_api.reviews_query(id=i)

    if response['total'] > 0:
        cols = list(response['reviews'][0].keys())
        res_df = pd.DataFrame(columns=cols)

        for rev in response['reviews']:
            res_df = res_df.append(rev, ignore_index=True)

        res_df = res_df[['id', 'text', 'rating']]

        Review_List = Review_List.append(res_df)
        print(len(Review_List))
    else:
        print("no reviews")

Review_List.to_csv('Yelp_Reviews.csv')
