import searchTweets

class SearchApiStream():

    #create a new fetcher
    searchApi = searchTweets()
    print "Running a fetcher."
    searchTweets.run()
