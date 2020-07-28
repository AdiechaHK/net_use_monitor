import scrapy
import time
import math
import re

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://3.7.153.175/vtpl/customer']

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
            txtUserName="HARIKRUSHNA_KRUSHNANAGAR",
            txtPassword="123456",
            ddlTheme="style5.css",
            DropDownList1="style.css",
            save="Log In"
        )

        for item in fields:
            q = response.css("#" + item + "::attr(value)")
            if (len(q) > 0):
                params[item] = q.extract()[0]

        yield scrapy.FormRequest(
            "http://3.7.153.175/vtpl/customer/Login.aspx?h8=1",
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
            print("=====================================================")
            print(mb)
            print("=====================================================")
            f = open("output.txt", "a")
            f.write(str(math.floor(time.time())))
            f.write(":" + mb + "\n")
            f.close()