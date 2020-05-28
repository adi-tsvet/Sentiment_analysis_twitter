
import sys,tweepy,csv,re
from textblob import TextBlob
from itertools import islice



class SentimentAnalysis():

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.tweet_id = []
        self.tweet_user = []
        self.tweetdict = {}

    def DownloadData(self,searchTerm,NoOfTerms=200):
        # authenticating
        consumerKey = 'OGSG8sCDSMsbA20Nxhv90s1EU'
        consumerSecret = 'CpmqIGZELFR8yIF451hVjIyDuPiEXBLym8uSC2Kuq4J6bSXWvi'
        accessToken = '1144135588380962817-9ZW7uIfOMJfLQ2yevlcUSum4BvVv3H'
        accessTokenSecret = 'jkjJm9tNlo6Y5riEdHvkdX9tAOgjNUyzP0SC6mPoEqJNq'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)



        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        #csvFile = open('result.csv', 'a')

        # Use csv writer
        #csvWriter = csv.writer(csvFile, delimiter='\n')


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            self.tweet_id.append(tweet.id)
            self.tweet_user.append(tweet.user.id)
            #print (self.user_id)
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            #self.tweetdict[tweet.user.id].append(analysis.sentiment.polarity)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1
        '''
        outtweets = [[tweet.user.id, tweet.id,tweet.text] for tweet in self.tweets]
        with open('%s_tweets.csv' % searchTerm, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(["User Id", "Tweet Id", "Tweet Text"])
            writer.writerows(outtweets)
        f.close()
        '''

        tweetdictpositive = sorted(self.tweetdict.items(), key=lambda item: item[1], reverse=True)
        tweetdictnegative = sorted(self.tweetdict.items(), key=lambda item: item[1])
        positive_items = self.take(5, tweetdictpositive.iteritems())
        negative_items = self.take(5, tweetdictnegative.iteritems())
        positive_user = positive_items.keys()
        negative_user = negative_items.keys()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        return polarity,positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,positive_user,negative_user;
        #self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
        #self.plotbargraph(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,NoOfTerms)

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def take(self, n, iterable):
        return list(islice(iterable, n))

'''
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        '''
'''
    def plotbargraph(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        index = sorted(labels)
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        #colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        plt.bar(index,sizes)
        plt.xlabel('Type', fontsize=5)
        plt.ylabel('% count', fontsize=5)
        plt.xticks(index, labels, fontsize=5, rotation=90)
        #plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        #plt.axis('equal')
        plt.tight_layout()
        plt.show()
        
        '''


'''
if __name__== "__main__":
    # input for term to be searched and how many tweets to search
    searchTerm = input("Enter Keyword/Tag to search about: ")
    NoOfTerms = int(input("Enter how many tweets to search: "))
    sa = SentimentAnalysis()
    sa.DownloadData(searchTerm,NoOfTerms)
'''