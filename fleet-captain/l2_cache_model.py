# -*- coding: utf-8 -*-
import logging
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from pynamodb.exceptions import PynamoDBConnectionError, TableDoesNotExist, DoesNotExist, PutError, UpdateError

logger = logging.getLogger(__name__)

class l2_cache_config(Model):
    class Meta:
        table_name = ''
        region = ''


    cacheKey = UnicodeAttribute(hash_key=True)

    @staticmethod
    def connect_to_dynamodb(table_name, region, host=None):
        logger.info("Connecting to DynamoDB | host={} | table={}".format(host, table_name))

        try:
            l2_cache_config.Meta.table_name = table_name
            l2_cache_config.Meta.region = region
            if host:
                l2_cache_config.Meta.host = host
            return True
        except (PynamoDBConnectionError, TableDoesNotExist, Exception) as exp:
            logger.exception("Failed to connect to DynamoDB | Host={} | Table={}".format(host, table_name))
            return False


    @staticmethod
    def get_record(cache_key):
        try:
            record = l2_cache_config.get(hash_key=cache_key)
            return record
        except DoesNotExist:
            return 0


l2_cache_config.connect_to_dynamodb("phenomics-l2-cache-b2", "ap-southeast-2")

