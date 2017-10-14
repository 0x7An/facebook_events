#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib3
import facebook
import requests
from configparser import ConfigParser
import argparse
import sys
from urllib.parse import quote

class FacebookScraper:
    def __init__(self, access_token, query, output_path):
        print("Procurando pelo termo:\n{}".format(query))

        self.access_token = access_token
        self.query = query
        self.output_path = output_path
        self.graph = facebook.GraphAPI(access_token=token, version = '2.10')
        events = self.graph.request("/search?q="+ quote(self.query) + "&type=event&limit=1")
        self.eventList = events["data"]

    def main(self):
        """Primary entry point of this script
           TODO: interate over the pages to get all the returned data.
        """
        for event in self.eventList:
            attenders = requests.get("https://graph.facebook.com/v2.10/"+event["id"]+"/attending?access_token="+token+"&limit=100")
            attenders_json = attenders.json()
            attenders_data = attenders_json["data"]
            # paging_data = attenders_json["paging"]
            with open(self.output_path, "w") as text_file:        
                for attender in attenders_data:
                    print("Nome: " + attender["name"] + " Id: " + attender["id"] +  "\n")
                    text_file.write("Nome: " + attender["name"] + " Id: " + attender["id"] +  "\n")

if __name__ == '__main__':
    """ Starting the script """
    config = ConfigParser()  
    config.read('config/config.ini')  
    token = config.get('auth', 'token')

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', help="The term that you want to search on facebook")
    parser.add_argument('-o', '--output_path', help='the path which you want to store the data')
    args = parser.parse_args()

    spider = FacebookScraper(token, args.query, args.output_path)
    spider.main()
    print("Pronto! Resultados salvos em :{}".format(args.output_path))