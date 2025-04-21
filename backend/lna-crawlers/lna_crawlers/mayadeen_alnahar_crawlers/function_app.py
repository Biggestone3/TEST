import datetime
import logging
import azure.functions as func
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 

#beanie requirements:
from beanie import init_beanie, Document, Indexed
from pydantic import EmailStr, Field

from typing import Annotated, Any, Self
from uuid import UUID, uuid4

from bson import ObjectId
from datetime import UTC, datetime

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


from enum import Enum #also built-in in the python 3.11
from my_types import Language # type: ignore

from news import AggregatedStory, Article, Source, User, UserPreferences 
app = func.FunctionApp()

@app.function_name(name="crawler_1")
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def crawler_1(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function executed.')
    mongo_uri = os.environ.get("MONGO_URI")

    garbage_links = set()
    good_links = set()
    dataset = []

    #UTILS

    def get_category_main_pages(main_url):
        html = requests.get(main_url)
        tags = BeautifulSoup(html.text, 'html.parser')
        menu_tags = tags.find('div', class_ = "menu")
        main_page_links = menu_tags.find_all('a', href = True)

        #let's process links so that later on we could scrape the main pages
        main_pages_to_scrape = normalize_links(main_url, main_page_links)

        #since we will scrape the main page too, we will add it to this list
        main_pages_to_scrape.append(main_url)
        return main_pages_to_scrape


    #PREPROCESS

    def get_language(content):
    # Common words in English articles
        dict_eng = {
            "the", "a", "an", "in", "on", "at", "by", "for", "with", "from", "to", "of",
            "and", "but", "or", "because", "if", "he", "she", "it", "they", "we", "you", "I",
            "is", "are", "was", "were", "have", "has", "do", "does", "can", "will", "time",
            "person", "year", "way", "day", "thing", "man", "world", "very", "not", "also", "more", "so"
        }

        # Common words in French articles
        dict_fr = {
            "le", "la", "les", "un", "une", "des", "à", "de", "en", "dans", "sur", "avec", "pour", "par",
            "et", "mais", "ou", "car", "donc", "il", "elle", "nous", "vous", "ils", "elles", "ce", "cette",
            "être", "avoir", "faire", "aller", "dire", "pouvoir", "temps", "personne", "année", "monde", "vie",
            "très", "pas", "aussi", "plus", "comme"
        }

        # Common words in Arabic articles (Arabic script)
        dict_ar = {
            "ال", "في", "على", "من", "إلى", "مع", "و", "أو", "لكن", "لأن", "هو", "هي", "نحن", "أنتم",
            "كان", "يكون", "قال", "فعل", "وقت", "إنسان", "يوم", "عام", "جدًا", "ليس", "أيضًا"
        }
        for word in content.split():
            if word in dict_eng:
                return Language.ENGLISH
            elif word in dict_fr:
                return Language.FRENCH
            elif word in dict_ar:
                return Language.ARABIC
        return Language.UNKNOWN

    def normalize_links(url, list_urls):
        for link in list_urls:
            if 'https://' not in str(link): #
                link = url + str(link) #
        return list_urls

    def unify_date_mayadeen(date):
        month_dict = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        if date.split()[2] in month_dict: #the date in the mayadeen xml is as follows: Tue, 25 Mar 2025 09:35:09 GMT
            #and in datetime the args are as follows: year, month #, #day, #hour, minute, second, tzinfo
            hour = date.split()[4]
            date_to_return = datetime(int(date.split()[3]),month_dict[date.split()[2]], int(date.split()[1]), int(hour.split(':')[0]), int(hour.split(':')[1]), int(hour.split(':')[2]),tzinfo= UTC)#essentially we should should add GMT not UTC
            return date_to_return 
        return False#in case we ended up with a false we'll leave the pydantic deal with it using default ...

    def unify_dates(date):
        month_dict = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April':4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }
        #we want the date format to be day-month-year 
        #most prob the year is the same as this year so we'll add 2025
        #note that we are solving the case where the date is january 26 ...
        #so we'll dissect based on space and we'll search in the dictionary
        #additionally the dates look like the following: '25-03-2025 | 09:52'
        #and sometimes gives: 'March 24'
        if date.split()[0] in month_dict:
            date = datetime(2025, month_dict[date.split()[0]],int(date.split()[1]), datetime.now().hour, 0, 0 , tzinfo = UTC)#hours and minutes are not available
            return date
        day_month_year = date.split('|')[0].split(':')
        hour_minute = date.split('|')[1]
        date = datetime(int(day_month_year[0].split('-')[2]), 
                        int(day_month_year[0].split('-')[1]), 
                        int(day_month_year[0].split('-')[0]), 
                        int(hour_minute.split(':')[0]), 
                        int(hour_minute.split(':')[1]), 
                        0,
                        tzinfo=UTC)        
        return date

    #SCRAPE / PROCESSING:
    def get_link_add_meta_data_to_dataset(main_url, news_tag):
        date = news_tag.find('div', class_ ="listingDate" ).contents[-1] #.contents will take the content of the direct children of this div as alist
        date = unify_dates(date.strip())
        category = news_tag.find('a', class_ = "type")
        title = news_tag.find('div', class_ = "listingTitle")

        link = title.find('a', href = True)
        scrape_link = ''
        if main_url not in link['href']:
            scrape_link = main_url + link ['href']
        else:
            scrape_link = link['href']
        if scrape_link not in good_links:
            title=str(title.text)
            summary="Something big happened!"
            url=str(scrape_link)
            publish_date=str(date) #there is the content and the language that are left
            return (scrape_link, title, summary, url, publish_date)
        return False



    def scrape_news(news_link): #where ar is the article
        # if news_link not in good_links:
            article_html = requests.get(news_link)
            article_tags = BeautifulSoup(article_html.text, 'html.parser')
            content = article_tags.find('div', class_='bodyText bodyContentMainParent')
            # dataset['Content'].append(str(content.text))
            # dataset['Language'].append(get_language(content.text))
            # dataset['Author'].append('Al Nahar')
            content = str(content.text)
            language = get_language(content)
            good_links.add(news_link)
            return content, language
        # return "", Language.FRENCH


    async def scrape_main_page(main_link):
        html = requests.get(main_link)
        tags = BeautifulSoup(html.text, 'html.parser')
        
        #we notice it is inside the tag div with class litingInfos:
        news = tags.find_all('div', class_ = "listingInfos") 
            

        for info in news:
            # if get_link_add_meta_data_to_dataset(main_link, info) == False: #handling the case where the link is already visited
            #     return False
            (scrape_link, title_i, summary_i, url_i, publish_date_i)  = get_link_add_meta_data_to_dataset(main_link, info) #
            try:
                #print("started scraping link: ", scrape_link)
                content_i, language_i = scrape_news(scrape_link)
                #print("successfully scraped the link")
                if(content_i != ""):#checking if the content is null i.e. could be a vid photo ...
                    #print("appending to dataset")
                    dataset.append(Article(
                            id=ObjectId(),
                            source_id= UUID('f67322c8-069c-43a2-9097-6805d56dd436'), # it is gonna be 2 specific values one for annahar and another for mayadeen
                            title=title_i,
                            content= content_i,
                            summary=summary_i,
                            url=url_i,
                            publish_date= publish_date_i,
                            language= language_i,
                    ))

            except:
                # print(scrape_link)
                #print("failed")
                garbage_links.add(scrape_link)


    #FINAL:
    async def scrape_alnahar(main_url):
        some_error = []
        main_pages = get_category_main_pages(main_url)
        for main_page in main_pages:
            try:
                main_page = main_url + main_page['href'] #
                await scrape_main_page(main_page)
            except:
                some_error.append(main_page)


    async def scrape_mayadeen_rss(xml):
        xml_almayadeen = requests.get(xml)
        almayadeen_tags = BeautifulSoup(xml_almayadeen.content, 'lxml-xml')
        news = almayadeen_tags.find_all('item')
        for info in news:
            title = info.find('title').text
            url = info.find('link').text
            if url not in good_links:
                date = info.find('pubDate').text
                category = info.find('category').text
                source = info.find('source').text

                #let's scrape the content
                content_page = requests.get(url)
                html_tags = BeautifulSoup(content_page.text, 'html.parser')
                content = html_tags.find('div', class_ = 'p-content')
                info = ''
                if content != None:
                    paragraphs = content.find_all('p', recursive = False) #recursive = False will take only p tags of depth 1
                    for paragraph in paragraphs:
                        info += paragraph.text.strip()
                dataset.append(Article(
                        id=ObjectId(),
                        source_id= UUID('8310fb18-4420-4cac-9330-9b178b8264dc'),#1 for mayadeen
                        title=title,
                        content= info,
                        summary="Something big happened!",
                        url=url,
                        publish_date=unify_date_mayadeen(date),
                        language= get_language(info),
                ))
    xml = 'https://www.almayadeen.net/feed.rss'

    async def add_to_db(dataset): #the dataset is a list of articles
        await dataset.save()

    #now the dataset has members of type Article so we need to initalize the beanie and start to add sstuff to the db
    async def init():
        try:
            #asynchrinous connecting:
            client = AsyncIOMotorClient(mongo_uri)
            db = client["my_db"]
            article = db["articles"]
            await init_beanie(database = db, document_models=[Article])
            logging.info("Connected to the db successful init_beanie")
        except:
            logging.error("error while establishing connection to the db")
        #writing to db 
        #with each function directly adding to the db as we go i.e. in the functions we will have an:
            #await Article( ... ).insert()
        #and at the end we will call this init() function to start running it using asyncio
        try:
            await scrape_mayadeen_rss(xml)
            #now we have the dataset filled with al mayadeen articles
            logging.info("successfully scraped mayadeen")

        except Exception as e:
            logging.error(f"{e} occured while scraping mayadeen")

        try:
            logging.info("started scraping annahar")
            await scrape_alnahar("https://www.annahar.com")
            logging.info("successfully scraped alnaha")
        except Exception as e:
            logging.error(f"{e} error occured while scraping alnahar")
        
        try:
            for article in dataset:
                await article.save()
        except:
            logging.error("error adding to the mongo db")

    try:
        logging.info("starting to run the beanie")
        asyncio.run(init())
    except:
        logging.error("error running the init function")
