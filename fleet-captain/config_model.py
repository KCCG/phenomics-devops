# -*- coding: utf-8 -*-
import logging
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from pynamodb.exceptions import PynamoDBConnectionError, TableDoesNotExist, DoesNotExist, PutError, UpdateError

logger = logging.getLogger(__name__)

class worker_config(Model):
    class Meta:
        table_name = ''
        region = ''


    workerID = UnicodeAttribute(hash_key=True)
    lastIndex = NumberAttribute()
    lastUpdateTime = NumberAttribute()
    isActive = BooleanAttribute()
    pipelinePort = UnicodeAttribute()

    @staticmethod
    def connect_to_dynamodb(table_name, region, host=None):
        logger.info("Connecting to DynamoDB | host={} | table={}".format(host, table_name))

        try:
            worker_config.Meta.table_name = table_name
            worker_config.Meta.region = region
            if host:
                worker_config.Meta.host = host
            return True
        except (PynamoDBConnectionError, TableDoesNotExist, Exception) as exp:
            logger.exception("Failed to connect to DynamoDB | Host={} | Table={}".format(host, table_name))
            return False


    @staticmethod
    def get_record(worker_id):
        try:
            record = worker_config.get(hash_key=worker_id)
            return record
        except DoesNotExist:
            return 0


worker_config.connect_to_dynamodb("worker-config", "ap-southeast-2")

