import tweepy
from tkinter import *
import User_info as user
import analysis as anlys
import user_analysis as user_anlys
import csv
import os.path
from os import path
import matplotlib
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#GLOBAL DECLARATION

ui = user.User_info()
analysis = anlys.SentimentAnalysis()
user_analysis = user_anlys.UserAnalysis()

win = Tk()



# AUTHENTICATION

consumer_key = "OGSG8sCDSMsbA20Nxhv90s1EU"
consumer_secret = "CpmqIGZELFR8yIF451hVjIyDuPiEXBLym8uSC2Kuq4J6bSXWvi"
access_token = "1144135588380962817-9ZW7uIfOMJfLQ2yevlcUSum4BvVv3H"
access_token_secret = "jkjJm9tNlo6Y5riEdHvkdX9tAOgjNUyzP0SC6mPoEqJNq"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#FUNCTION

def search_keyword():
    global frame4,frame3,select;
    keyword_text  = keyword.get()
    print("keyword : ",keyword_text)
    user_data = ui.Import_user_data(keyword_text)

    frame3 = Frame(win)
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Text(frame3, yscrollcommand=scroll.set, height=6)
    scroll.config(command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT, fill=BOTH, expand=1)
    select.insert(END,user_data[0])
    select.insert(END,user_data[10])

    if (path.exists('%s.csv' % (keyword_text))):
        #print("under if")
        csvFile = open('%s.csv' % (keyword_text), 'w')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"')
        csvWriter.writerow(user_data)
    else:
        csvFile = open('%s.csv' % (keyword_text), 'a')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"')
        csvWriter.writerow(["user_name",
                     "user_username",
                     "user_followers_count",
                     "user_listed_count",
                     "user_following",
                     "user_favorites",
                     "user_verified",
                     "user_default_profile",
                     "user_location",
                     "user_time_zone",
                     "user_statuses_count",
                     "user_description",
                     "user_geo_enabled",
                     "user_contributors_enabled"])
        csvWriter.writerow(user_data)
    print("Wrote tweets by %s to CSV." % keyword_text)
    #print(keyword_text)
    frame4 = Frame(win)
    frame4.pack()
    btnplot = Button(frame4, text=" Plot Graph ", command=tweet_analysis)
    btnplot.pack(side=LEFT)

def tweet_analysis():
    global frame4,positive_user,negative_user;
    keyword_text = keyword.get()

    polarity,positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,positive_user,negative_user = analysis.DownloadData(keyword_text)
    Text_box = Text(frame4, height=2, width=30)
    Text_box.pack()
    Text_box.insert(END,"Polarity of the keyword : \n")
    Text_box.insert(END,str(polarity))
    # Create a Tkinter variable
    positive = StringVar(frame4)
    negative = StringVar(frame4)

    # Dictionary with options
    positive.set(positive_user[0])  # set the default option
    negative.set(negative_user[0])

    popupMenupos = OptionMenu(frame4, positive, *positive_user)

    Label(frame4, text="Positive Influencer").pack()
    popupMenupos.pack()
    popupMenuneg = OptionMenu(frame4, negative, *negative_user)
    Label(frame4, text="Negative Influencer").pack()
    popupMenuneg.pack()
    plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm)


def plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms=200):
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
    fig = matplotlib.figure.Figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    patches, texts = ax.pie(sizes, colors=colors, startangle=90)
    ax.legend(patches, labels, loc="best")
    #fig.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    #ax.axis('equal')
    circle = matplotlib.patches.Circle((0, 0), 0.7, color='white')
    ax.add_artist(circle)
    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.get_tk_widget().pack()
    canvas.draw()

def search_user():
    global usertext,username_text,frame5,frame6
    username_text = username.get()
    print("Username : ", username_text)
    user_obj = api.get_user(user)
    user_data = [user_obj.name,
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
    #user_data = ui.Import_user_data(username)
    frame5 = Frame(win)
    frame5.pack(side=RIGHT)
    scroll = Scrollbar(frame5, orient=VERTICAL)
    usertext = Text(frame5, yscrollcommand=scroll.set, height=6)
    scroll.config(command=usertext.yview)
    scroll.pack(side=RIGHT, fill=Y)
    usertext.pack(side=LEFT, fill=BOTH, expand=1)

    usertext.insert(END, user_data[0])
    usertext.insert(END, user_data[10])

    usertext.insert(END, "USERNAME : " + user_data[1] + "\n")
    usertext.insert(END, "FOLLOWERS COUNT : " + user_data[2] + "\n")

    usertext.insert(END, 'FOLLOWING COUNT : ' + user_data[4] + "\n")
    usertext.insert(END, 'FAVOURITES : ' + user_data[4] + "\n")
    usertext.insert(END, 'LOCATION : ' + user_data[7] + "\n")
    usertext.insert(END, 'STATUSES COUNT : ' + user_data[8] + "\n")
    usertext.insert(END, 'DESCRIPTION : ' + user_data[9] + "\n")

    frame6 = Frame(win)
    frame6.pack(side=RIGHT)
    btnplotuser = Button(frame6, text=" Plot Graph ", command=user_analysis)
    btnplotuser.grid(column=6, row=4)


def user_analysis():
    global frame6;

    polarity,positive, wpositive, spositive, negative, wnegative, snegative, neutral,count = user_analysis.get_all_tweets(username_text)
    Text_box = Text(frame6, height=2, width=30)
    Text_box.pack()
    Text_box.insert(END, "Polarity of the keyword : \n")
    Text_box.insert(END, str(polarity))
    plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, username_text)

def refresh():
    keyword.delete(0, END)
    frame3.destroy()
    frame4.destroy()

def reset():
    usertext.delete(0, END)
    frame6.destroy()



#MAIN UI

def make_window():
    global frame1,frame2,keyword,frame5,username;


    frame1 = Frame(win)
    frame1.pack(side=LEFT, fill=Y)
    Label(frame1, text="Any Keyword").grid(row=0, column=0, sticky=W)
    keyword = Entry(frame1, bd=1)
    keyword.grid(row=0, column=1, sticky=W)

    canvas = Canvas()
    canvas.create_line(400, 0, 400, 800)

    frame5 = Frame(win)
    Label(frame1, text="User Search").grid(row=0, column=5, sticky=W)
    username = Entry(frame5, bd=1)
    username.grid(row=1, column=5, sticky=W)
    frame5.pack(side=RIGHT, fill=Y)
    btnsearch2 = Button(frame5, text=" Search User ", command=search_user)
    btnrefresh2 = Button(frame5, text="RESET", command=reset)
    btnsearch2.grid(column=6, row=0)
    btnrefresh2.grid(column=7, row=0)

    frame2 = Frame(win)
    frame2.pack()
    btnsearch = Button(frame2, text=" Search by Keyword ", command=search_keyword)
    btnrefresh = Button(frame2, text="RESET", command=refresh)
    btnsearch.grid(column=2, row=0)
    btnrefresh.grid(column=3, row=0)



    return win

if __name__== "__main__":

    win = make_window()
    win.geometry('800x800')
    win.mainloop()




