import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["imdb.com"]

    # Bypass User-Agent because imdb.com doesn't accept default Scrapy User-Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    def start_requests(self):
        yield scrapy.Request(url = "https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc", headers = {
            'User-Agent': self.user_agent
        })

    # LinkExtractor parameters:
    # allow => if the link contains the word x then follow it
    # deny => if the link contains the word x then don't follow it
    # restrict_xpaths => if the link is in a tag found in the xpath string then follow it (example: //a[@class="active"], follow every link in <a> with class active)
    # restrict_css => if the if the link is in a tag found in the css string then follow it
    # with restrict_xpaths don't put @href at the end, the crawler will automatically search for that attribute
    rules = (
        # The rules are called in order
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback="parse_item", follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"), follow=True, process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        
        yield {
            'title': response.xpath("//h1[@data-testid='hero__pageTitle']/span/text()").get(),
            'year': response.xpath("//div[@class='sc-dffc6c81-0 iwmAVw']/ul/li[1]/a/text()").get(),
            'duration': response.xpath("//div[@class='sc-dffc6c81-0 iwmAVw']/ul/li[3]/text()").get(),
            'genre': response.xpath("//a[@class='ipc-chip ipc-chip--on-baseAlt']/span/text()").get(),
            'rating': response.xpath("(//span[@class='sc-bde20123-1 iZlgcd'])[1]/text()").get(),
            'movie_url': response.url
        }
