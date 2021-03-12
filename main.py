import pandas as pd
import plotly.express as px
import kaleido
import os
import tweepy
from time import sleep

#variables 
imgpath= "path"
consumer_key = "key"
consumer_secret = "key_secret"
access_token = "token"
access_token_secret = "token_secret"

#passes authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#creates Twitter API-Object
api = tweepy.API(auth)

def make_dataframe():
    global dataframe
    #gets iss api information
    url = "http://api.open-notify.org/iss-now.json"
    dataframe = pd.read_json(url)
    #configures dataframe
    dataframe['latitude'] = dataframe.loc['latitude', 'iss_position']
    dataframe['longitude'] = dataframe.loc['longitude', 'iss_position']
    dataframe.reset_index(inplace=True)
    dataframe = dataframe.drop(['index', 'message'], axis=1)  
    
#draws map with iss position
def draw_map(dataframe):
    map = px.scatter_geo(dataframe, lat='latitude', lon='longitude')
    #saves map as Jpeg
    map.write_image(imgpath)
   

#tweets Map and Position 
def tweet_photos(api, dataframe):
    long = dataframe.loc[0, 'longitude']
    lat = dataframe.loc[0, 'latitude']
    i = True
    while i:
        status = ("The ISS is at: \n Long: %s / lat: %s" % (long, lat))
        try:
            api.update_with_media(filename=imgpath,status=status)
            print ("Tweeted!")
        except Exception as e:
            print ("fehler: %s"%str(e))
            break
        i = False

#calls functions
def main():
    #loops functions every 60min
    while True:
        make_dataframe()
        draw_map(dataframe)
        tweet_photos(api, dataframe)
        sleep(3600)

if __name__ == "__main__":
    main()
