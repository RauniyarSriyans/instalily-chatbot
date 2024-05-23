# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

# useful for handling different item types with a single interface
import os

# import psycopg2
from itemadapter import ItemAdapter

# from scrapy.exceptions import DropItem

# from .utils.db import get_db_conn


class AllModelsPartsPipeline:
    def open_spider(self, spider):
        # self.conn = get_db_conn()

        self.dir = os.path.abspath(
            os.path.join(os.path.join(__file__, "../../../out/models"))
        )
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def close_spider(self, spider):
        # self.conn.close()
        pass

    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)

        # write to json
        with open(f'{self.dir}/{item_adapter.get("id")}.jsonl', "w") as file:
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            file.write(line)

        # cursor = self.conn.cursor()

        # model_data = {
        #     "name": item_adapter.get("name"),
        #     "id": item_adapter.get("id"),
        #     "link": item_adapter.get("link"),
        #     "parts": item_adapter.get("parts"),
        # }

        # try:
        #     cursor.execute(
        #         """
        #         INSERT INTO models (name, id, link) VALUES (%(name)s, %(id)s, %(link)s) ON CONFLICT(id) DO UPDATE SET name = %(name)s, id = %(id)s, link = %(link)s
        #         """,
        #         model_data,
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error inserting models: {e}")

        # # insert the parts
        # try:
        #     parts_args_str = ", ".join(
        #         cursor.mogrify(
        #             "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        #             (
        #                 part.get("id", None),
        #                 part.get("name", None),
        #                 part.get("price", None),
        #                 part.get("link", None),
        #                 part.get("manufacturer_part_number", None),
        #                 part.get("manufactured_by", None),
        #                 part.get("description", None),
        #                 part.get("fixes", None),
        #                 part.get("works_with_appliances", None),
        #                 part.get("works_with_brands", None),
        #                 part.get("part_replaces", None),
        #                 part.get("part_videos", None),
        #             ),
        #         ).decode("utf-8")
        #         for part in model_data["parts"]
        #     )

        #     cursor.execute(
        #         """
        #         INSERT INTO parts (id, name, price, link, manufacturer_part_number, manufactured_by, description, fixes, works_with_appliances, works_with_brands, part_replaces, part_videos) VALUES
        #         """
        #         + parts_args_str
        #         + """
        #         ON CONFLICT(id) DO NOTHING
        #         """
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error inserting parts: {e}")

        # try:
        #     models_parts_arg_str = ", ".join(
        #         cursor.mogrify(
        #             "(%s, %s)",
        #             (part.get("id", None), model_data["id"]),
        #         ).decode("utf-8")
        #         for part in model_data["parts"]
        #     )

        #     cursor.execute(
        #         """
        #         INSERT INTO models_parts (part_id, model_id) VALUES
        #         """
        #         + models_parts_arg_str
        #         + """
        #         ON CONFLICT(part_id, model_id) DO NOTHING
        #         """
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error inserting models_parts: {e}")

        # self.conn.commit()

        return item


class ModelPipeline:
    def open_spider(self, spider):
        # self.conn = get_db_conn()

        self.dir = os.path.abspath(
            os.path.join(os.path.join(__file__, "../../../out/models"))
        )
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def close_spider(self, spider):
        # self.conn.close()
        pass

    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)

        # write to json
        with open(f'{self.dir}/{item_adapter.get("id")}.jsonl', "w") as file:
            print("made file at", f'{self.dir}/{item_adapter.get("id")}.jsonl')
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            file.write(line)

        # cursor = self.conn.cursor()

        # model_data = {
        #     "name": item_adapter.get("name"),
        #     "id": item_adapter.get("id"),
        #     "link": item_adapter.get("link"),
        #     "parts": item_adapter.get("parts"),
        # }

        # try:
        #     cursor.execute(
        #         """
        #         INSERT INTO models (name, id, link) VALUES (%(name)s, %(id)s, %(link)s) ON CONFLICT(id) DO UPDATE SET name = %(name)s, id = %(id)s, link = %(link)s
        #         """,
        #         model_data,
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error inserting models: {e}")

        # # insert the parts
        # parts_args_str = ", ".join(
        #     cursor.mogrify(
        #         "(%s, %s, %s, %s)",
        #         (
        #             part["partselect_number"],
        #             part["part_name"],
        #             part["part_link"],
        #             None if part["part_price"] == "" else part["part_price"],
        #         ),
        #     ).decode("utf-8")
        #     for part in model_data["parts"]
        # )

        # try:
        #     cursor.execute(
        #         """
        #         INSERT INTO parts (id, name, link, price) VALUES
        #         """
        #         + parts_args_str
        #         + """
        #         ON CONFLICT(id) DO NOTHING
        #         """
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error inserting parts: {e}")

        # try:
        #     model_parts_data = ", ".join(
        #         cursor.mogrify(
        #             "(%s, %s)", (part["partselect_number"], model_data["id"])
        #         ).decode("utf-8")
        #         for part in model_data["parts"]
        #     )
        #     cursor.execute(
        #         """
        #         INSERT INTO models_parts (part_id, model_id) VALUES
        #         """
        #         + model_parts_data
        #         + """
        #         ON CONFLICT(part_id, model_id) DO NOTHING
        #         """,
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"Error inserting models_parts: {e}")

        self.conn.commit()

        return item


class PartDetailsPipeline:
    def open_spider(self, spider):
        # self.conn = get_db_conn()

        self.dir = os.path.abspath(
            os.path.join(os.path.join(__file__, "../../../out/parts"))
        )
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def close_spider(self, spider):
        # self.conn.close()
        pass

    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)

        # write to json
        with open(f'{self.dir}/{item_adapter.get("id")}.jsonl', "w") as file:
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            file.write(line)

        # cursor = self.conn.cursor()

        # data = {
        #     "id": item_adapter.get("id"),
        #     "manufacturer_part_number": item_adapter.get(
        #         "manufacturer_part_number", None
        #     ),
        #     "manufactured_by": item_adapter.get("manufactured_by", None),
        #     "description": item_adapter.get("description", None),
        #     "fixes": item_adapter.get("fixes", None),
        #     "works_with_appliances": item_adapter.get("works_with_appliances", None),
        #     "works_with_brands": item_adapter.get("works_with_brands", None),
        #     "part_replaces": item_adapter.get("part_replaces", None),
        #     "part_videos": item_adapter.get("part_videos", None),
        # }

        # try:
        #     cursor.execute(
        #         """
        #         UPDATE parts SET manufacturer_part_number = %(manufacturer_part_number)s, manufactured_by = %(manufactured_by)s, description = %(description)s, fixes = %(fixes)s, works_with_appliances = %(works_with_appliances)s, works_with_brands = %(works_with_brands)s, part_replaces = %(part_replaces)s, part_videos = %(part_videos)s WHERE id = %(id)s
        #         """,
        #         data,
        #     )
        # except psycopg2.Error as e:
        #     raise DropItem(f"error updating parts: {e}")

        # self.conn.commit()

        return item
