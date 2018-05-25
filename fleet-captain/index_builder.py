import logging
import requests
import csv
import queue
from l2_cache_model import l2_cache_config

logging.basicConfig(
    level=logging.INFO, filename='logs/index_builder.log'
)

class index_builder():
    candidates = []
    logger = logging.getLogger(__name__)
    pipeline_service_url = 'http://52.62.22.150:9080/query/?pageSize=10&pageNo=1&includeHistorical=true'


    def run(self):
        self.read_candidates();
        # print(self.candidates)

        tasks = queue.Queue(200)
        counter = 1
        for search_item in self.candidates:
            search_items = [search_item]
            filter_items = []
            logging.info("Processing search Item {}:{}".format(counter, search_item))
            cache_key, request_params = self._get_params (search_items, filter_items)
            response = requests.post(self.pipeline_service_url, json=request_params)
            if response.status_code != 200 or response.text == '[]':
                logging.info("Error in processing query.")
            else:
                response_map = response.json()
                if "filters" in response_map:
                    response_filters = response_map["filters"]
                    for filter in response_filters[:min(100, len(response_filters))]:
                        if "id" in filter:
                            cache_key, rp = self._get_params(search_items, [filter["id"]])
                            if self.should_process(cache_key):
                                tasks.put(rp)
                self.call_search_for_filter_tasks(tasks)
            counter = counter + 1


    def call_search_for_filter_tasks(self, tasks):
        while not tasks.empty():
            params = tasks.get()
            response = requests.post(self.pipeline_service_url, json=params)
            if response.status_code != 200 or response.text == '[]':
                logging.info("Error in processing query.")

    def should_process(self, key):
        logging.info("checking key in dynamo:{}".format(key))
        record = l2_cache_config.get_record(key)
        if record is not 0:
            logging.info("Key exists in dynamo:{}".format(key))
            return False
        else:
            logging.info("key does not exist in dynamo:{}".format(key))
            return True

    @staticmethod
    def _get_params(search_items, filter_items):

        cache_key = "{0}-{1}".format("S", ','.join(search_items))
        data = {
            "searchItems": search_items
        }

        if len(filter_items) > 0:
            data.update({"filterItems": filter_items})
            filter_key = ','.join(filter_items)
            cache_key = cache_key + ";F-" + filter_key
        return cache_key, data

    def read_candidates(self):
        with open('L2Candidates.txt', 'r') as f:
            for line in csv.reader(f, dialect="excel-tab"):
                self.candidates.append(line[1])



x = index_builder()
x.run()

