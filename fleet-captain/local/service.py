import boto3
import logging
logger = logging.getLogger(__name__)

def disable_affinity():
    client = boto3.client('ecs')
    for x in range(0,10):
        service_name = 'affinity-worker-' + str(x)
        print("Stopping service:{}".format(service_name))
        client.update_service(cluster= "phenomics-affinity-fleet", service= service_name, desiredCount=0)



def enable_affinity():
    client = boto3.client('ecs')
    for x in range(1,10):
        service_name = 'affinity-worker-' + str(x)
        print("Starting service:{}".format(service_name))
        client.update_service(cluster= "phenomics-affinity-fleet", service= service_name, desiredCount=1)


def disable_pipeline():
    client = boto3.client('ecs')
    for x in range(0,8):
        service_name = 'fleet-worker-' + str(x)
        task_name = 'phenomics-pipeline-task-worker' + str(x)
        print("Stopping service:{}".format(service_name))
        client.update_service(cluster= "phenomics-ingestion-fleet", service= service_name, desiredCount=0,taskDefinition=task_name)



def enable_pipeline():
    client = boto3.client('ecs')
    for x in range(1,8):
        service_name = 'fleet-worker-' + str(x)
        task_name = 'phenomics-pipeline-task-worker' + str(x)
        print("Starting service:{}-> task:{}".format(service_name, task_name))
        client.update_service(cluster= "phenomics-ingestion-fleet", service= service_name, desiredCount=1,taskDefinition=task_name)


enable_affinity()
