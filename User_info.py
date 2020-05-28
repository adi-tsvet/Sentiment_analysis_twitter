import tweepy

consumerKey = 'OGSG8sCDSMsbA20Nxhv90s1EU'
consumerSecret = 'CpmqIGZELFR8yIF451hVjIyDuPiEXBLym8uSC2Kuq4J6bSXWvi'
accessToken = '1144135588380962817-9ZW7uIfOMJfLQ2yevlcUSum4BvVv3H'
accessTokenSecret = 'jkjJm9tNlo6Y5riEdHvkdX9tAOgjNUyzP0SC6mPoEqJNq'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)



class User_info():

    def Import_user_data(self,user):

        user_obj = api.get_user(user)
        user_info = [user_obj.name,
                     user_obj.screen_name,
                     user_obj.followers_count,
                     user_obj.listed_count,
                     user_obj.friends_count,
                     user_obj.favourites_count,
                     user_obj.verified,
                     user_obj.default_profile,
                     user_obj.location,
                     user_obj.time_zone,
                     user_obj.statuses_count,
                     user_obj.description,
                     user_obj.geo_enabled,
                     user_obj.contributors_enabled]
        return user_info


