# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

# from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页种的文章url并交给scrapy下载后并进行解析
        2. 获取下一页url并交给scrapy进行下载，下载完成后交给parse
        """

        # 获取文章列表页种的文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first('')
            image_url = parse.urljoin(response.url, image_url)
            post_url = post_node.css("::attr(href)").extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.detail_parse)

        # 获取下一页url并交给scrapy进行下载，下载完成后交给parse
        next_url = response.css(".next.page-numbers::attr(href)").extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def detail_parse(self, response):
        """
        提取文章详情
        """
        # 使用xpath选择器
        article_item = JobBoleArticleItem()

        # 标题
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # 发表时间
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first('').strip()\
            .replace(' ·', '')
        # 标签
        tag_list_tmp = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list_tmp if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)
        # 封面图
        front_image_url = response.meta.get('front_image_url', '')
        # 点赞数
        post_nums_tmp = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first('')
        post_nums = int(post_nums_tmp) if post_nums_tmp else 0
        # 收藏数
        fav_nums_tmp = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first('')
        match_re = re.match(r'.*?(\d+).*?', fav_nums_tmp)
        fav_nums = int(match_re.group(1)) if match_re else 0
        # 评论数
        comment_nums_tmp = response.xpath("//a[@href='#article-comment']/text()").extract_first('')
        match_re = re.match(r'.*?(\d+).*?', comment_nums_tmp)
        comment_nums = int(match_re.group(1)) if match_re else 0
        # 评论内容
        comments_dict = {}
        name_list = []
        name_list_tmp = response.css('div .comments li .cmnt-header .cmnt-meta')
        for tmp in name_list_tmp:
            name = tmp.css('span ::text').extract_first('')
            name_list.append(name)

        comment_list = []
        comment_list_tmp = response.css('div .comments li .cmnt-body')
        for tmp in comment_list_tmp:
            comment = ''.join(tmp.css('p ::text').extract())
            comment_list.append(comment)
        for name, comment in zip(name_list, comment_list):
            comments_dict[name] = comment
        # 正文内容
        content = response.xpath("//div[@class='entry']").extract_first('')

        article_item['title'] = title
        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['front_image_url'] = [front_image_url]
        article_item['tags'] = tags
        article_item['post_nums'] = post_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['comments'] = comments_dict
        article_item['content'] = content

        # 通过item loader加载item
        # front_image_url = response.meta.get('front_image_url', '')
        # item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        # item_loader.add_xpath('create_date', "//p[@class='entry-meta-hide-on-mobile']/text()")
        # item_loader.add_value('url', response.url)
        # item_loader.add_value('url_object_id', get_md5(response.url))
        # item_loader.add_value('front_image_url', [front_image_url])
        # item_loader.add_xpath('tags', "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        # item_loader.add_css('post_nums', ".vote-post-up h10::text")
        # item_loader.add_xpath('fav_nums', "//span[contains(@class, 'bookmark-btn')]/text()")
        # item_loader.add_xpath('comment_nums', "//a[@href='#article-comment']/text()")
        # item_loader.add_xpath('content', "//div[@class='entry']")
        # article_item = item_loader.load_item()
        # article_item['comments'] = comments_dict

        yield article_item
