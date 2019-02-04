#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:50:28 2019

@author: louis-alexisdubief
"""
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


keyWords = ['gadget','gadgets','technology','tech','innovation','free shipping','goods','invention','gimmick','hi tech','high tech','science','scientific','electronic','device','new','future']
stopWordsEN = set(stopwords.words('english'))

class Strategies:

    def __init__(self,api):
        self.api = api

    def followBack(self):
        print(' -------------------------------------------------')
        print('|           starting follow back strategy        |')
        print(' ------------------------------------------------ ')
        followings = self.api.getFollowings('BestDailyGadge2',nb=self.api.getNumberFollowing('BestDailyGadge2'))
        followers = self.api.getFollowers('BestDailyGadge2',nb=self.api.getNumberFollowers('BestDailyGadge2'))
        for following in followings.username:
            if following not in followers.username:
                self.api.unFollow(following)
                followings = followings[followings.username != following]

    def followInterest(self):
        print(' -------------------------------------------------')
        print('|        starting follow interest strategy       |')
        print(' ------------------------------------------------ ')
        followings = self.api.getFollowings('BestDailyGadge2',nb=self.api.getNumberFollowing('BestDailyGadge2'))
        for following in followings.username:
            nbFollowers = self.api.getNumberFollowers(following)
            bio = [i for i in word_tokenize(followings[followings.username == following].shortBio.iloc[0].lower()) if i not in stopWordsEN]
            if nbFollowers > 10000 or len(list(set(keyWords) & set(bio))) >= 1:
                followersfollowing = self.api.getFollowers(following,100)
                for followers in followersfollowing.username:
                    nbfollowersfollower = self.api.getNumberFollowers(followers)
                    biofollower = [i for i in word_tokenize(followersfollowing[followersfollowing.username == followers].shortBio.iloc[0].lower()) if i not in stopWordsEN]
                    if nbfollowersfollower > 20000 or len(list(set(keyWords) & set(biofollower))) >= 1:
                        self.api.follow(followers)



