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
