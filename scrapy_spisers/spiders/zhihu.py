# -*- coding: utf-8 -*-
import scrapy
import json,re
from scrapy import Request,FormRequest
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy_spisers.items import zhihu_question_item,zhihu_answer_item
from scrapy_spisers.util.common import getMd5
import time

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 定制settings
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
    }

    def get_zhihu_answer_url(self, question_id):
        return 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'.format(
            question_id)

    def parse(self, response):
        print("开始解析")
        with open("zhuhu.html", "wb") as f:
            f.write(response.body)
        links = response.css('a::attr(href)').extract()
        # print (links)
        pattern = re.compile(r'(^/question/(\d+)(/|$).*)')
        for link in links:
            # print (link)
            match_obj = re.match(pattern,link)
            if match_obj:
                print ("success")
                question_id = match_obj.group(2)
                yield Request(url=urljoin(response.url, link),meta={"question_id":question_id},callback=self.parse_question,headers=self.headers)
                zhihu_answer_url = self.get_zhihu_answer_url(str(question_id))
                # time.sleep(5)
                yield Request(url=zhihu_answer_url, callback=self.parse_answer, headers=self.headers)
            else:
                print("fail")

    def parse_question(self, response):
        question_id = response.meta.get("question_id","")
        title = response.xpath('//div[@class="QuestionPage"]/meta[@itemprop="name"]/@content').extract_first("")
        url = response.css('div.QuestionPage meta[itemprop="url"] ::attr(content)').extract_first("")
        keywords = response.css('div.QuestionPage meta[itemprop="keywords"] ::attr(content)').extract_first("")
        answerCount = response.css('div.QuestionPage meta[itemprop="answerCount"] ::attr(content)').extract_first("0")
        commentCount = response.css('div.QuestionPage meta[itemprop="commentCount"] ::attr(content)').extract_first("0")
        dateCreated = response.css('div.QuestionPage meta[itemprop="dateCreated"] ::attr(content)').extract_first("")
        dateModified = response.css('div.QuestionPage meta[itemprop="dateModified"] ::attr(content)').extract_first("")
        visitsCount = response.css('div.QuestionPage meta[itemprop="zhihu:visitsCount"] ::attr(content)').extract_first("0")
        followerCount = response.css('div.QuestionPage meta[itemprop="zhihu:followerCount"] ::attr(content)').extract_first("0")
        content = response.css('div.QuestionRichText--expandable span.RichText ::text').extract_first("")

        question_item = zhihu_question_item()
        question_item['question_id'] = question_id
        question_item['title'] = title
        question_item['url'] = url
        question_item['url_id'] = getMd5(url)
        question_item['keywords'] = keywords
        question_item['answerCount'] = int(answerCount)
        question_item['commentCount'] = int(commentCount)
        question_item['dateCreated'] = dateCreated
        question_item['dateModified'] = dateModified
        question_item['visitsCount'] = int(visitsCount)
        question_item['followerCount'] = int(followerCount)
        question_item['content'] = content
        yield question_item

    def parse_answer(self,response):
        #处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = zhihu_answer_item()
            answer_item["answer_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]

            yield answer_item

        if not is_end:
            time.sleep(10)
            yield Request(next_url, callback=self.parse_answer)



    # def get_xsrf(self, response):
    #     pattern = re.compile(r'.*name="_xsrf" value="(.*?)"')
    #     match = re.findall(pattern, response.text)
    #     if match:
    #         _xsrf = match[0]
    #     else:
    #         _xsrf = ""
    #     capt_url = "https://www.zhihu.com/captcha.gif?type=login&lang=cn"
    #     yield Request(capt_url, meta={"_xsrf":_xsrf}, callback=self.get_capt)
    #
    # def login(self, response):
    #     print("登录请求状态：" + str(response.status))
    #     ret_json = json.loads(response.text, encoding='utf-8')
    #     msg = ret_json.get("msg", "")
    #     print("登录返回结果：" + msg)
    #     if msg == "登录成功":
    #         print("开始从首页爬取")
    #         for url in self.start_urls:
    #             yield Request(url, dont_filter=True)
    #         # start_url = "http://www.zhihu.com/"
    #         # yield Request(start_url, callback=self.parse_detail)
    #
    # def get_capt(self, response):
    #     _xsrf = response.meta.get("_xsrf","")
    #     print("获取验证码图片状态：" + str(response.status))
    #     with open("zhuhu.png", "wb") as f:
    #         f.write(response.body)
    #     a = input("请输入倒立的文字的x坐标：")  # 范围[0-200].比如：20,100,150
    #     x_nums = a.split(',')
    #     input_points = [[x, 20] for x in x_nums]
    #     captcha = {"img_size": [200, 44], "input_points": input_points}
    #     captcha_str = json.dumps(captcha)
    #     login_url = "https://www.zhihu.com/login/phone_num"
    #     post_data = {
    #         "_xsrf": _xsrf,
    #         "phone_num": "13246856469",
    #         "password": "",
    #         "captcha_type": "cn",
    #         "captcha": captcha_str
    #     }
    #     yield FormRequest(login_url,callback=self.login, method='POST',formdata=post_data)
    #
    # def parse_detail(self,response):
    #     print(response.body)
    #     with open("zhihu.html","wb") as f:
    #         f.write(response.body)
    #     #todo:提取url，继续爬取

