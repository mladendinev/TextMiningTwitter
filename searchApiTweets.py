import twitter
import json

#auth credentials
consumer_key = 'qFrfx5pbJwrL2QxfzvLVufRVi'
consumer_secret = '2Sq6lLxYZhMK2s5N57X5kvVDa8TTGFcgIuqBJpZ9Dufqv0NqWj'
access_token = '3749211929-7efi0f7VxlllNEhpWslKTZqmt3bAqfEpZF0ZQlU'
access_secret = 'OqFqVtS7srb0fuSIGXks9o5qFc8FNi5ScjkKogFLAWILG'

auth = twitter.oauth.OAuth(access_token,access_secret,consumer_key,consumer_secret)

twitter_api = twitter.Twitter(auth=auth)

query1 = 'insomnia OR other ppls OR other ppl'

count = 100

search_results = twitter_api.search.tweets(q=query1, count= count)

statuses = search_results['statuses']

for _ in range(5):
	print "Length  of statuses", len(statuses)
	try:
		next_results = search_results['search_metadata']['next_results']
	except KeyError, e:
		break

		kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

print json.dumps(statuses[0], indent=1)