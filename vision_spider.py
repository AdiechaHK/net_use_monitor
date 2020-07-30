import configparser
import scrapy
import urllib
import time
import math
import re
import os

class VisionSpider(scrapy.Spider):
    name = 'vision_spider'
    start_urls = ['http://3.7.153.175/vtpl/customer']
    user = 'HK_HOME'

    def __init__(self):
        super(VisionSpider, self).__init__()
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'config.ini')
        print("==============================================")
        print("Config file path: " + filename)
        print("==============================================")
        self.config = configparser.ConfigParser()
        self.config.read(filename)


    def parse(self, response):
        fields = [
            '__LASTFOCUS',
            '__EVENTTARGET',
            '__EVENTARGUMENT',
            '__VIEWSTATE',
            '__VIEWSTATEGENERATOR',
            '__EVENTVALIDATION'
        ]

        params = dict(
            txtUserName=self.config.get(self.user, 'USERNAME'),
            txtPassword=self.config.get(self.user, 'PASSWORD'),
            ddlTheme="style5.css",
            DropDownList1="style.css",
            save="Log In"
        )


        for item in fields:
            q = response.css("#" + item + "::attr(value)")
            if (len(q) > 0):
                params[item] = q.extract()[0]


        formurl = urllib.parse.urljoin(response.url, response.css("#Form1::attr(action)").extract()[0])

        yield scrapy.FormRequest(
            formurl,
            self.after_logged_in,
            formdata=params,
            headers={})


    def after_logged_in(self, response):
        yield scrapy.Request(
            "http://3.7.153.175/vtpl/customer/AccountViewPlan.aspx",
            self.scrap_data)

    def scrap_data(self, response):
        # scrapy.shell.inspect_response(response, self)
        id = "#ContentPlaceHolder1_tbAdditonal_tpPlan_gdPlan_lblRemain_0::text"
        q = response.css(id)
        if (len(q) > 0):
            val = q.extract()[0]
            mb = re.findall('\\d+', val)[0]
            filepath = os.path.join(self.config.get('DEFAULT', 'OUTPUT'), (self.user + "_NET_USAGE.txt").lower())
            print("================================================")
            print("Writting Data to file:" + filepath + " [" + mb + "]")
            print("================================================")
            f = open(filepath, "a")
            f.write(str(math.floor(time.time())))
            f.write(":" + mb + "\n")
            f.close()