import boto3
import logging
logger = logging.getLogger(__name__)

class cluster:
    def find_name(arn):
        index=  arn.rfind('/')
        name = arn[index + 1: len(arn)]
        splits = name.split(':')
        return splits[0]

    def delete_tasks(worker_id):
        logger.info("Cluster is called to delete worker tasks with id: {}".format(worker_id))

        client = boto3.client('ecs')
        x=client.list_tasks(cluster= "phenomics-ingestion-fleet")
        tasks = x['taskArns']
        # logger.info("Found task list: {}".format(tasks))
        tasks_defs = client.describe_tasks(
            cluster= "phenomics-ingestion-fleet",
            tasks=tasks
        )

        for task_def in tasks_defs['tasks']:
          try:
            host_port = (task_def['containers'][0]['networkBindings'][0]['hostPort'])
            name_arn=  task_def['taskDefinitionArn']
            name = cluster.find_name(name_arn)
            task_arn = task_def['taskArn']
            # print("{}:{} -- {}".format(host_port, name, task_arn))

            if(name == 'phenomics-pipeline-task-worker'+ worker_id ):
                logger.info("Worker to be deleted: {}:{}:{}".format(worker_id, host_port, task_arn ))
                response = client.stop_task(
                      cluster="phenomics-ingestion-fleet",
                      task=task_arn,
                      reason='Not working actively'
                  )
                logger.info("Worker deleted: {}".format(worker_id))
                return host_port
          except:
              logger.info("exception in task:".format(task_def))



