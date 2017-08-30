#Source Code adopted by u/dantheman1129
# A Reddit bot that posts explanation of XKCD comic strips posted in comments
# The explanation is extracted from http://explainxkcd.com
# Created by Ayush Dwivedi (/u/kindw)
# License: MIT License

from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4

path = '/home/dan/commented.txt'
# Location of file where id's of already visited comments are maintained

header = '**Info about this item:**\n'
footer = '\n*---This info was extracted from [DarkSouls.Wikidot](http://www.darksouls.wikidot.com) | Bot created by u/dantheman1129 *'
# Text to be posted along with item description


def authenticate():
   
    print('Authenticating...\n')
    reddit = praw.Reddit('soulsbot', user_agent = 'web:Souls-Bot (by u/dantheman1129)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetchdata(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
   
    return data


def run_soulsbot(reddit):
   
    print("Getting 10,000,000,000 comments...\n")
   
    for comment in reddit.subreddit('test').comments(limit =10000000000 ):
        match = re.findall("[a-z]*[A-Z]*[0-9]*!Soulsbot", comment.body)
        print(match)
        if match:
            print('Link found in comment with comment ID: ' + comment.id)
            wikidot_url = match[0]
            print('Link: ' + wikidot_url)

            url_obj = urlparse(wikidot_url)
            souls_id = str((url_obj.path.strip("/")))
            myurl = 'http://www.darksouls.wikidot.com/' + str(souls_id)
            print(myurl)
           
            file_obj_r = open(path,'r')
                       
            try:
                explanation = fetchdata(myurl)
            except:
                print('Exception!!! Possibly incorrect item name...\n')
               
            else :
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(header + explanation + footer)
                   
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
           
            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    reddit = authenticate()
    while True:
        run_soulsbot(reddit)


if __name__ == '__main__':
    main()
