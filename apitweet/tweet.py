
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 16:32:11 2019

@author: louis-alexisdubief
"""
import datetime
import selenium.common.exceptions as selexcept


class Tweet():

    def __init__(self,divClassTweet,driver):
        self.driver = driver
        self.base = divClassTweet
        self.username = self.base.find_element_by_css_selector('.username').text.split('@')[1]
        self.date = datetime.datetime.strptime(self.base.find_element_by_css_selector('.tweet-timestamp').get_attribute('title'),'%I:%M %p - %d %b %Y')
        self.content = self.base.find_element_by_css_selector('.TweetTextSize').text
        self.nbLikes =  self.parseString(self.base.find_elements_by_css_selector('.ProfileTweet-actionCountForPresentation')[3].text)
        self.nbRetweets =  self.parseString(self.base.find_elements_by_css_selector('.ProfileTweet-actionCountForPresentation')[1].text)
        self.nbReplies =  self.parseString(self.base.find_elements_by_css_selector('.ProfileTweet-actionCountForPresentation')[0].text)
        self.popularity = self.nbRetweets + self.nbLikes

    def __str__(self):
        return self.username + ' - ' + str(self.date) + ' - ' + self.content

    def like(self):
        print('-------------------------------------------------')
        print('liking tweet of ',self.username,' ...')
        likes = self.base.find_elements_by_css_selector('.IconContainer.js-tooltip')[4]
        try:
            likes.click()
        except selexcept.ElementNotVisibleException:
            print('you are already liking this tweet of ',self.username)
            pass
        except selexcept.WebDriverException:
            self.driver.execute_script("arguments[0].click();", likes)
            print('success liking the tweet of ',self.username)
            pass

    def unlike(self):
        print('-------------------------------------------------')
        print('unliking tweet of ',self.username,' ...')
        likes = self.base.find_elements_by_css_selector('.IconContainer.js-tooltip')[5]
        try:
            likes.click()
        except selexcept.ElementNotVisibleException:
            print('you are already not liking this tweet of ',self.username)
            pass
        except selexcept.WebDriverException:
            self.driver.execute_script("arguments[0].click();", likes)
            print('success unliking the tweet of ',self.username)
            pass

    def getParseContent(self):
        words = word_tokenize(self.content)
        return [word for word in words if word not in set(self.language)]

    def parseString(self,nb):
        if nb == '':
            return 0
        if 'k' in nb.lower():
            return float(nb.lower().split('k')[0])*1000
        elif 'm' in nb.lower():
            return float(nb.lower().split('m')[0])*1000000
        else:
            return int(nb)





