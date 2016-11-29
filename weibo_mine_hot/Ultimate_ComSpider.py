# coding=utf-8
import requests
import json
import scrapy
import re
import writers
import get_weibo_cookie
import time
from retrying import retry
import Normalize_date_time
import Refresh_cookie
import urllib
def space(s):
    return re.sub('\s+', '', s)

class weibocom(object):
    def __init__(self):
        self.maxpage=50
        self.baseurl='http://s.weibo.com/weibo'
        self.session=get_weibo_cookie.login()
        self.db=writers.Content()

        self.headers={
                      'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36'
        }
        #with open('PycharmProjects/TestZhu/tjufe/weibo_mine_hot/cookies','r') as f:
        with open('cookies','r') as f:
            cook=f.readlines()[0]
        self.cookie={'Cookie':cook}
    def start_html(self,name):
        self.name=urllib.quote(name)
        urls=['{}/{}&nodup=1&page={}'.format(self.baseurl,self.name,page) for page in range(1,self.maxpage)]
        for each in urls:
            html=requests.get(each,cookies=self.cookie,headers=self.headers).text
            time.sleep(10)
            self.parse(html)

    def parse(self, response):
        htmls = re.findall('STK\.pageletM\.view\((.*?)\)<', response, re.S)
        try:
            rule_html = self.parse_html_by_pid(htmls)
        except:
            rule_html = None
        if rule_html:
            self.extract_one_page(rule_html)
        else:
            print htmls

    # @retry(_stop_max_attempt_number=2)
    def parse_html_by_pid(self, htmls):
        for each in htmls:
            pid = json.loads(each)['pid']
            if pid == u'pl_weibo_direct':
                return json.loads(each)['html']
        print 'cookie unuse?'
        Refresh_cookie.main()
        print 'restart...'
        self.start_html(self.name)

    def extract_one_page(self, html):
        con_lst = scrapy.Selector(text=html).xpath('.//div[@class="WB_cardwrap S_bg2 clearfix"]')
        length=len(con_lst)
        print 'the length of constant page is {}'.format(length)
        if length<8:
            Refresh_cookie.main()
            print 'restart...'
            self.start_html(self.name)

        for each in con_lst:
            msg_id = each.xpath('.//div[@mid]/@mid').extract_first()
            msg_url_action_data = each.xpath('.//ul[@class="feed_action_info feed_action_row4"]/li[2]/a[@action-data]/@action-data').extract_first()
            msg_url = re.search('url=(.*?)&',msg_url_action_data).group(1)
            msg_user_id= re.search('weibo.com/(.*?)/',msg_url).group(1)
            content_lst = each.xpath('.//p[@class="comment_txt"]')
            msg_content = "".join([p.xpath('string(.)').extract_first().strip() for p in content_lst])
            contain = each.xpath('.//div[@class="feed_from W_textb"]')
            pretime = contain.xpath('.//a[@node-type="feed_list_item_date"]/text()').extract_first()
            try:
                msg_time = Normalize_date_time.normalize_datetime(pretime)
            except:
                msg_time=None
                pass
            resource = contain.xpath('.//a[@rel="nofollow"]/text()').extract_first()

            msg_up= msg_cmt = msg_resport = msg_collection = 0
            comment_msg = each.xpath('.//div[@class="feed_action clearfix"]/ul/li')
            for every in comment_msg:
                value = every.xpath('string(.)').extract_first()
                if u'收藏' in value:
                    try:
                        msg_collection = re.search('(\d+)', value).group(1)
                    except:
                        pass
                if u'转发' in value:
                    try:
                        msg_resport = re.search('(\d+)', value).group(1)
                    except:
                        pass
                if u'评论' in value:
                    try:
                        msg_cmt = re.search('(\d+)', value).group(1)
                    except:
                        pass

                if every.xpath('.//a[@title]/@title').extract_first() == u'赞':
                    msg_up = every.xpath('string(.)').extract_first()

            is_resport = each.xpath('.//div[@class="comment"]')
            msg_resport_url = ''
            if is_resport:
                msg_resport_url_source = is_resport.xpath(
                    './/a[@suda-data="key=tblog_search_weibo&value=weibo_zhuan_p"]/@href').extract_first()
                msg_resport_url = re.search('(^.*?)\?', msg_resport_url_source).group(1)
            m=(self.name,msg_id,msg_url,msg_user_id,msg_content,msg_time,resource,msg_up,msg_resport,msg_cmt,msg_collection,msg_resport_url)
            print m
            self.db.insertIntoDB1(m)
            if msg_resport_url:
                 self.extract_one_article(msg_resport_url)

    @retry(stop_max_attempt_number=3)
    def extract_html_bydomid(self,url):
        response=requests.get(url,headers=self.headers,cookies=self.cookie).text
        htmls=re.findall('<script>FM\.view\((.*?)\)</script>', response, re.S)
        for html in htmls:
            try:
                if re.match(u'Pl_Official_WeiboDetail__\d+', json.loads(html)['domid']):
                    return json.loads(html)['html']
            except:
                continue
        print 'dont exist weibodetail'

    def extract_one_article(self,url):
        try:
            html=self.extract_html_bydomid(url)
            selector=scrapy.Selector(text=html)
            weibo_id=selector.xpath('.//div[@class="WB_from S_txt2"]/a/@name').extract_first()
            weibo_time_pre = selector.xpath('.//div[@class="WB_from S_txt2"]/a[@node-type="feed_list_item_date"]/text()').extract_first()
            weibo_time = Normalize_date_time.normalize_datetime(weibo_time_pre)
            weibo_content=space(selector.xpath('.//div[@node-type="feed_list_content"]')[0].xpath('string(.)').extract_first())
            weibo_up = selector.xpath('.//span[@node-type="like_status"]')[0].xpath('string(.)').extract_first()
            weibo_report = selector.xpath('.//span[@class="line S_line1" and @node-type="forward_btn_text"]')[0].xpath('string(.)').extract_first()
            weibo_comment = selector.xpath('.//span[@class="line S_line1" and @node-type="comment_btn_text"]')[0].xpath('string(.)').extract_first()
            try:
                weibo_up = re.search('(\d+)', weibo_up).group(1)
            except:
                weibo_up = 0
            try:
                weibo_report = re.search('(\d+)', weibo_report).group(1)
            except:
                weibo_report = 0
            try:
                weibo_comment = re.search('(\d+)', weibo_comment).group(1)
            except:
                weibo_comment=0
            m=(self.name,url,weibo_id,weibo_time,weibo_content,weibo_up,weibo_report,weibo_comment)
            self.db.inserIntoDB2(m)
            print m
        except:
            pass



p=weibocom()
p.start_html('张清扬')
