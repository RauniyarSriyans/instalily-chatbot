from typing import Any

import scrapy
from scrapy.loader import ItemLoader

from ..items import ModelItem
from ..pipelines import ModelPipeline


class ModelSpider(scrapy.Spider):
    name = "model"
    allowed_domains = ["partselect.com"]
    custom_settings = {"ITEM_PIPELINES": {ModelPipeline: 300}}

    def __init__(
        self,
        model_number: str,
        **kwargs: Any,
    ):
        super(ModelSpider, self).__init__(**kwargs)

        self.model_number = model_number

    def start_requests(self):
        self.url = f"https://www.partselect.com/Models/{self.model_number}"

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        # we get redirected to homepage if the model doesn't exist
        if response.url == "https://www.partselect.com/":
            print(
                f"Model {self.model_number} is not found, redirected from: {self.url}, to: {response.url}"
            )
            return

        self.item = ItemLoader(ModelItem(), response)
        self.parts = []

        name = response.css("h1.title-main::text").get().split("-")[0].strip()
        self.item.add_value("name", name)

        model_number = response.url.split("/")[-2]
        self.item.add_value("id", model_number)

        self.item.add_value("link", response.url)

        yield response.follow(url=f"{self.url}/Parts", callback=self.parse_model_parts)

    def parse_model_parts(self, response):
        for response_part in response.css("div.mega-m__part"):
            num_link_name_selector = response_part.css("a.bold.mb-1.mega-m__part__name")
            partselect_number = (
                num_link_name_selector.xpath("following-sibling::div[1]/text()")
                .get()
                .strip()
            )

            part_name = num_link_name_selector.xpath("text()").get()
            part_link = response.urljoin(num_link_name_selector.xpath("@href").get())
            part_price = "".join(
                response_part.css("div.mega-m__part__price *::text").extract()
            ).strip()
            self.parts.append(
                {
                    "partselect_number": partselect_number,
                    "part_link": part_link,
                    "part_price": part_price,
                    "part_name": part_name,
                }
            )

        #! could be used for parellely making request
        last_link = int(
            response.xpath(
                '//ul[@class="pagination js-pagination"]//li[position() = (last() - 1)]//a/text()'
            )
            .get()
            .strip()
        )

        next_page = response.css("ul.pagination li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_model_parts)
        else:
            self.item.add_value("parts", self.parts)
            yield self.item.load_item()
