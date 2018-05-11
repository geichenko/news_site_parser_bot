from pymongo import MongoClient
from dateutil import parser


class MDB(object):
    def __init__(self, u_name: str, u_pass: str, db_name: str, collection: str):
        mongo_url = f"mongodb+srv://{u_name}:{u_pass}@clustertest-x6pax.mongodb.net/test"
        client = MongoClient(mongo_url)
        db = client[db_name]
        self.collection = db[collection]

    def write(self, post: dict or list):
        if type(post) is list:
            self.collection.insert_many(post)
        else:
            self.collection.insert_one(post)

    def get_entries(self, formula: dict={}) -> list:
        return self.collection.find(formula).sort([('date', -1)])

    def get_last_entries(self) -> dict:
        return list(self.collection.find().sort([('date', -1)]).limit(1))[0]

    def get_entries_by_date(self, date: str) -> list:
        """
        :param date: YYYY-MM-DD
        :return: list of entries, [dicts]
        """
        date_start = parser.parse(date).timestamp()
        date_end = parser.parse(date).timestamp() + 86400
        return self.get_entries({"date": {"$gte": date_start, "$lt": date_end}})

    def get_entries_by_tag(self, tag_name: str):
        return self.get_entries({"tags": tag_name})

    def get_entries_by_tag_and_date(self, tag_name:str, date: str) -> list:
        """
        :param tag_name:
        :param date: YYYY-MM-DD
        :return: list of entries, [dicts]
        """
        date_start = parser.parse(date).timestamp()
        date_end = parser.parse(date).timestamp() + 86400
        return self.get_entries({"tags": tag_name, "date": {"$gte": date_start, "$lt": date_end}})
