import tweepy
import shutil
import pathlib
import os
from datetime import date

X_ACCESS_KEY = "xxxxxxxx"
X_ACCESS_SECRET = "xxxxxxxx"
X_CONSUMER_KEY = "xxxxxxxx"
X_CONSUMER_SECRET = "xxxxxxxx"
X_BEARER_TOKEN = "xxxxxxxx"

# Authenticate to X
auth = tweepy.OAuthHandler(X_CONSUMER_KEY, X_CONSUMER_SECRET)
auth.set_access_token(
    X_ACCESS_KEY,
    X_ACCESS_SECRET,
)
# this is the syntax for twitter API 2.0. It uses the client credentials that we created
newapi = tweepy.Client(
    bearer_token=X_BEARER_TOKEN,
    access_token=X_ACCESS_KEY,
    access_token_secret=X_ACCESS_SECRET,
    consumer_key=X_CONSUMER_KEY,
    consumer_secret=X_CONSUMER_SECRET,
)

# Create API object using the old twitter APIv1.1
api = tweepy.API(auth)

# adding the tweet content 
sampletweet = "yeah i am testing it with images and done it with success \n\n\n\n #testing"

# image in the same directory
for images in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    # check if the image ends with png and take the first image that you find
    if images.endswith(".jpeg"):
        img = images
        break
today = date.today()
# upload the media using the old api
media = api.media_upload(os.path.join(os.path.abspath(os.path.dirname(__file__)), img))
# create the tweet using the new api. Mention the image uploaded via the old api
post_result = newapi.create_tweet(text=sampletweet, media_ids=[media.media_id])
# the following line prints the response that you receive from the API. You can save it or process it in anyway u want. I am just printing it.
print(post_result)
# get the file extension. This would be png by default but I was experimenting with different images. Will update this if required
file_extension = pathlib.Path(img).suffix

# Define the path for the archives directory
archives_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "archives")

# Create the archives directory if it doesn't exist
if not os.path.exists(archives_dir):
    os.makedirs(archives_dir)
# Move the image to archives folder and rename it as per the date it was uploaded. I am only adding one post per day so this makes more sense
shutil.move(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), img),
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        archives_dir,
        today.strftime("%Y%m%d") + file_extension,
    ),
)
