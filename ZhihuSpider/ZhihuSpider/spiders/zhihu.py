# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time

from ZhihuSpider.items import ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['https://www.zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v4/questions/29814297/answers']

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/" \
                       "answers?sort_by=default&include=data%5B%2A%5D." \
                       "is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2" \
                       "Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2" \
                       "Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2" \
                       "Creshipment_settings%2Ccomment_permission%2Cmark_infos%2" \
                       "Ccreated_time%2Cupdated_time%2Crelationship.is_author%2" \
                       "Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3" \
                       "Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2" \
                       "Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3" \
                       "Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.'
                      '0.3071.115 Safari/537.36',
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    }

    def parse_answer(self, response):
        answer_json = json.loads(response.text)
        next_url = answer_json['paging']['next']
        is_end = answer_json['paging']['is_end']
        for answer in answer_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['answer_id'] = answer['id']
            answer_item['author_id'] = answer['author']['id']
            answer_item['author_name'] = answer['author']['name']
            answer_item['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(answer['created_time']))
            answer_item['updated_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(answer['updated_time']))
            answer_item['question_title'] = answer['question']['title']
            answer_item['question_id'] = answer['question']['id']
            answer_item['voteup_count'] = answer['voteup_count']
            answer_item['comment_count'] = answer['comment_count']
            answer_item['content'] = answer['content']
            answer_item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer, dont_filter=True)

    def start_requests(self):
        yield scrapy.Request(self.start_answer_url.format(29814297, 20, 0),
                               headers=self.headers, callback=self.parse_answer)