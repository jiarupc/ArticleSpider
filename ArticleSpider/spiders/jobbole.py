# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

from ArticleSpider.items import JobboleArticleItem

from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 1. 获取文章列表中的 URL，交给scrapy 下载，解析函数进行具体字段解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_img_url" : image_url}, callback=self.parse_detail)

        # 2. 获取下一页的 URL，交给 scrapy 下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        article_item = JobboleArticleItem()

        # 提取文章的具体字段
        title = response.css(".entry-header h1::text").extract()
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css("span.vote-post-up h10::text").extract()[0]
        front_img_url = response.meta.get("front_img_url", "")  # 文章封面图

        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums = response.css("a[href='#article-comment'] span").extract()[0]
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.css(".entry").extract()

        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)
        article_item["create_date"] = create_date
        article_item["front_img_url"] = [front_img_url]
        article_item["praise_nums"] = praise_nums
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["tags"] = tags
        article_item["content"] = content

        yield article_item
