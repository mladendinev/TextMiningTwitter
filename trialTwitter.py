import twitter


consumer_key = 'qFrfx5pbJwrL2QxfzvLVufRVi'
consumer_secret = '2Sq6lLxYZhMK2s5N57X5kvVDa8TTGFcgIuqBJpZ9Dufqv0NqWj'
access_token = '3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU'
access_secret = 'OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG'

auth = twitter.oauth.OAuth(access_token,access_secret,consumer_key,consumer_secret)

twitter_api = twitter.Twitter(auth=auth)

print twitter_api