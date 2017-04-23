import scrapy
import re

class CSS(scrapy.Spider):
    def parse(self, response):
        # css 选择器提取字段
        title = response.css(".entry-header h1::text").extract()
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css("span.vote-post-up h10::text").extract()[0]

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

        pass