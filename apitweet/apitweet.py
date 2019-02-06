#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 20:00:06 2019

@author: louis-alexisdubief
"""
from selenium import webdriver
import pandas as pd
import time
import numpy as np
import selenium.common.exceptions as selexcept
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import json

from apitweet.strategies import Strategies
from apitweet.tweet import Tweet

chromedriverPath = r'/Users/louis-alexisdubief/Documents/BestDailyGadget/python/'
basePath = r'http://twitter.com/'


class Apitweet():
    def __init__(self, email, password):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://twitter.com/BestDailyGadge2')
        time.sleep(2)
        self.connect(email, password)

    def errorQuit(self, message):
        print(message)
        time.sleep(2)
        self.driver.quit()

    def connect(self, mail, password):
        print('-------------------------------------------------')
        print('waiting for connection to ', mail)
        self.driver.find_element_by_name(
            'session[username_or_email]').send_keys(mail)
        self.driver.find_element_by_name(
            'session[password]').send_keys(password)
        self.driver.find_element_by_xpath(
            "//input[@type='submit' and @value='Log In']").click()
        time.sleep(2)
        print('connected')

    def getNumberFollowers(self, username):
        print('-------------------------------------------------')
        print('getting number of followers of ', username)
        self.driver.get(basePath + username)
        time.sleep(2)
        try:
            followers = self.driver.find_element_by_css_selector(
                '.ProfileNav-item--followers')
            followers = int(followers.find_element_by_css_selector(
                '.ProfileNav-value').get_attribute('data-count'))
            print(username, ' has ', followers, ' followers')
            return followers
        except selexcept.NoSuchElementException:
            print(username, ' has 0 followers')
            return 0

    def getNumberFollowing(self, username):
        print('-------------------------------------------------')
        print('getting number of people that ', username, ' is following')
        self.driver.get(basePath + username)
        time.sleep(2)
        try:
            following = self.driver.find_element_by_css_selector(
                '.ProfileNav-item--following')
            following = int(following.find_element_by_css_selector(
                '.ProfileNav-value').get_attribute('data-count'))
            print(username, ' is following ', following, ' people')
            return following
        except selexcept.NoSuchElementException:
            print(username, ' is following 0 people')
            return 0

    def getNumberTweets(self, username):
        print('-------------------------------------------------')
        print('getting number of tweets of ', username)
        self.driver.get(basePath + username)
        time.sleep(2)
        try:
            tweets = self.driver.find_element_by_css_selector(
                '.ProfileNav-item--tweets')
            tweets = int(tweets.find_element_by_css_selector(
                '.ProfileNav-value').get_attribute('data-count'))
            print(username, ' has ', tweets, ' tweets')
            return tweets
        except selexcept.NoSuchElementException:
            print(username, ' has 0 tweets')
            return 0

    def getNumberLikes(self, username):
        print('-------------------------------------------------')
        print('getting number of likes of ', username)
        self.driver.get(basePath + username)
        time.sleep(2)
        try:
            likes = self.driver.find_element_by_css_selector(
                '.ProfileNav-item--likes')
            likes = int(likes.find_element_by_css_selector(
                '.ProfileNav-value').get_attribute('data-count'))
            print(username, ' has ', likes, ' likes')
            return likes
        except selexcept.NoSuchElementException:
            print(username, ' has 0 likes')
            return 0

    def getFollowings(self, username, nb=100):
        print('-------------------------------------------------')
        print('getting list of ', nb, ' people that ',
              username, ' is following ...')
        self.driver.get(basePath + username + '/following')
        time.sleep(2)
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            grids = self.driver.find_element_by_css_selector(
                '.GridTimeline-items').find_elements_by_css_selector('.Grid.Grid--withGutter')
            if new_height == last_height or len(grids)*6 > nb:
                break
            last_height = new_height
        items = []
        for grid in grids:
            for case in grid.find_elements_by_css_selector('.ProfileCard'):
                items.append(case)
        if len(items) < nb:
            nb = len(items)
        df = []
        for i in range(nb):
            username = items[i].get_attribute('data-screen-name')
            title = items[i].find_element_by_css_selector('.fullname').text
            shortbio = items[i].find_element_by_css_selector(
                '.ProfileCard-bio').text
            df.append([username, title, shortbio])
        df = pd.DataFrame(df, columns=['username', 'title', 'shortBio'])
        print('done. Found ', nb, ' followings')
        return df.sample(frac=1)

    def getFollowers(self, username, nb=100):
        print('-------------------------------------------------')
        print('getting list of ', nb, ' people that follow ', username, ' ...')
        self.driver.get(basePath + username + '/followers')
        time.sleep(2)
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            grids = self.driver.find_element_by_css_selector(
                '.GridTimeline-items').find_elements_by_css_selector('.Grid.Grid--withGutter')
            if new_height == last_height or len(grids)*6 > nb:
                break
            last_height = new_height
        items = []
        for grid in grids:
            for case in grid.find_elements_by_css_selector('.ProfileCard'):
                items.append(case)
        if len(items) < nb:
            nb = len(items)
        df = []
        for i in range(nb):
            username = items[i].get_attribute('data-screen-name')
            title = items[i].find_element_by_css_selector('.fullname').text
            shortbio = items[i].find_element_by_css_selector(
                '.ProfileCard-bio').text
            df.append([username, title, shortbio])
        df = pd.DataFrame(df, columns=['username', 'title', 'shortBio'])
        print('done. Found ', nb, ' followers')
        return df.sample(frac=1)

    def follow(self, username):
        print('-------------------------------------------------')
        print('trying to follow ', username, ' ...')
        if username == 'BestDailyGadge2':
            print('you can\'t follow yourself')
            return
        self.driver.get(basePath + username)
        time.sleep(2)
        followButton = self.driver.find_element_by_css_selector(
            '.EdgeButton.EdgeButton--secondary.EdgeButton--medium.button-text.follow-text')
        try:
            followButton.click()
        except selexcept.ElementNotVisibleException:
            print('you are already following ', username)
            pass
        else:
            print('success ! you are now following ', username)

    def unFollow(self, username):
        print('-------------------------------------------------')
        print('trying to unfollow ', username, ' ...')
        self.driver.get(basePath + username)
        time.sleep(2)
        followButton = self.driver.find_element_by_css_selector(
            '.EdgeButton.EdgeButton--primary.EdgeButton--medium.button-text.following-text')
        try:
            followButton.click()
        except selexcept.ElementNotVisibleException:
            print('you are already not following ', username)
            pass
        else:
            print('success ! now you are not following ', username, ' anymore')

    def getLastTweets(self, username, nb=5):
        print('-------------------------------------------------')
        print('getting last ', nb, ' tweets of ', username, ' ...')
        self.driver.get(basePath + username)
        time.sleep(2)
        for i in range(math.ceil(nb/20)):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        gridTweets = self.driver.find_elements_by_css_selector('.tweet')
        tweets = []
        for i in range(nb):
            tweets.append(Tweet(gridTweets[i], self.driver))
        return tweets
