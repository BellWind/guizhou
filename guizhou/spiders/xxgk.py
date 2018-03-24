# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy import Request
import requests

class XxgkSpider(scrapy.Spider):
    name = 'xxgk'
    allowed_domains = ['www.gzgov.gov.cn']
    start_urls = ['http://www.gzgov.gov.cn/xxgk/jbxxgk/zfjg/']
    sid = 1

    def parse(self, response):
        sel = Selector(response)
        dep_list = sel.xpath('//*[@class="bmxxgkml_list"]/ul/script/text()').extract()
        re1 = '(<a href=")'
        re2 = '(http://www.gzgov.gov.cn/xxgk/jbxxgk/zfjg/.*?)'
        re3 = '(")'
        rg = re.compile(re1+re2+re3, re.IGNORECASE|re.DOTALL)

        # tmpm = rg.search(dep_list[0])
        # yield Request(tmpm.group(2), callback=self.parser2)

        for dep in dep_list:
            m = rg.search(dep)
            if m:
                dep_url = m.group(2)
                yield Request(dep_url, callback=self.parser2)

    def parser2(self, response):
        sel = Selector(response)
        dep = sel.xpath('/html/head/title/text()').extract_first()
        dep = dep.replace('贵州省人民政府-','')
        head = sel.xpath('//*[@class="bmgk_con"]')

        for var in head:
            name = var.xpath('div[2]/p[1]/text()').extract_first()
            # print(name)

            prourl = var.xpath('div[2]/p[2]/a/@href').extract_first()
            tmpres = requests.get(prourl)
            tmpres.encoding = "utf-8"
            tmpsel = Selector(tmpres)
            protext = tmpsel.xpath('//*[@class="zw-con"]/text()').extract()
            pro = self.normalWord(protext)
            # print(pro)

            imgtext = var.xpath('div[1]/script/text()').extract_first()
            imgurl = self.getImgUrl(imgtext)
            # print(imgurl)

            worktext = var.xpath('div[2]/script[2]/text()').extract_first()
            work = self.getWork(worktext)
            # print(work)

            self.store_to_file(name, imgurl, pro, dep, work, response.url)

    def normalWord(self, text):
        ret = ''
        for str in text:
            if(str != None):
                ret += ''.join(str.split())
        return ret

    def getImgUrl(self, imgtext):
        pt = '((https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])'
        rg = re.compile(pt, re.IGNORECASE | re.DOTALL)
        m = rg.search(imgtext)
        imgurl = ''
        if m:
            imgurl += m.group(0)
            imgurl = imgurl.rstrip('\\')
        # if(imgurl == ''): # 算了，导不出来正确的正则表达式
        #     imgurl = 'http://www.gzgov.gov.cn/'
        #     re12 = '(<img src=\"/)'
        #     re22 = '(.*?)'
        #     re23 = '(\")'
        #     rg2 = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
        #     m2 = rg2.search(imgtext)
        #     if m2:
        #         imgurl += m2.group(2)
        return imgurl

    def getWork(self, worktext):
        re1 = '(var  str=")'
        re2 = '(.*?)'
        re3 = '(";)'
        rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
        m = rg.search(worktext)
        work = ''
        if m:
            work += m.group(2)
        return work

    def store_to_file(self, name, imgurl, pro, dep, work, infourl):

        filename = 'tmp.txt'
        with open(filename, 'a') as f:
            # print(self.sid)
            # self.sid += 1
            try:
                f.write(name.strip())
            finally:
                pass
            f.write('\n')
            try:
                f.write(imgurl)
            finally:
                pass
            f.write('\n')
            try:
                f.write(pro)
            finally:
                pass
            f.write('\n')
            try:
                f.write(dep)
            finally:
                pass
            f.write('\n')
            try:
                f.write(work)
            finally:
                pass
            f.write('\n')
            try:
                f.write(infourl)
            finally:
                pass
            f.write('\n')
        f.close()
