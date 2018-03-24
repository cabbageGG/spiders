# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy_spisers.util.common import get_random_ip

class ScrapySpisersSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    #随机更换User-Agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)   #  等价于self.ua.ua_type --- 如：ua.random
        request.headers.setdefault('User-Agent',get_ua())

class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        # ip 代理： 随机取出一个可以使用的ip代理。
        ip = get_random_ip()
        print (request.url)
        # request.meta["proxy"] = ip

from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="C:/opt/chromedriver.exe")
        super(JSPageMiddleware,self).__init__()

    def process_request(self, request, spider):
        # 使用浏览器
        print(request.url)
        print(request.url)
        if request.url == "http://www.zhihu.com/":
            # browser = webdriver.Chrome(executable_path="C:/opt/chromedriver.exe")
            self.browser.get(request.url)
            self.browser.find_element_by_css_selector("div.SignFlow-accountInput.Input-wrapper input.Input").send_keys(
                "13246856469")
            self.browser.find_element_by_css_selector(
                "div.SignFlow-password div.SignFlowInput div.Input-wrapper input.Input").send_keys("68ba70ma92wo")
            self.browser.find_element_by_css_selector("button.SignFlow-submitButton").click()
            import time
            time.sleep(3)
            print("浏览器访问")
            for i in range(10):
                self.browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(3)
            print (self.browser.page_source)
            return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8", request=request)

