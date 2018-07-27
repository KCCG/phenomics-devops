import boto3
import logging

logger = logging.getLogger(__name__)


class cluster:
    def find_name(arn):
        index = arn.rfind('/')
        name = arn[index + 1: len(arn)]
        splits = name.split(':')
        return splits[0]

    def delete_tasks(worker_id):
        logger.info("Cluster is called to delete worker tasks with id: {}".format(worker_id))
        affinity_port = cluster.delete_affinity_taks(worker_id)
        pipeline_port = cluster.delete_pl_taks(worker_id)
        return "{}:{}".format(pipeline_port, affinity_port)

    def delete_pl_taks(worker_id):
        cluster_name = "phenomics-ingestion-fleet"
        logger.info("Processing pipeline deletion: {}".format(worker_id))
        client = boto3.client('ecs')
        x = client.list_tasks(cluster=cluster_name)
        tasks = x['taskArns']
        tasks_defs = client.describe_tasks(
            cluster=cluster_name,
            tasks=tasks
        )
        pipeline_task_arn = ""
        pipeline_port = ""
        for task_def in tasks_defs['tasks']:
            try:
                host_port = (task_def['containers'][0]['networkBindings'][0]['hostPort'])
                name_arn = task_def['taskDefinitionArn']
                name = cluster.find_name(name_arn)
                task_arn = task_def['taskArn']
                if name == 'phenomics-pipeline-task-worker' + str(worker_id):
                    pipeline_task_arn = task_arn
                    pipeline_port = host_port
            except:
                logger.info("exception in task:".format(task_def))
        logger.info("Pipeline Worker to be deleted: {}:{}:{}".format(worker_id, pipeline_port, pipeline_task_arn))
        response = client.stop_task(
            cluster=cluster_name,
            task=pipeline_task_arn,
            reason='Not working actively'
        )
        logger.info("Pipeline worker deleted: {}".format(worker_id))
        return "{}".format(pipeline_port)

    def delete_affinity_taks(worker_id):
        logger.info("Processing affinity deletion: {}".format(worker_id))
        client = boto3.client('ecs')
        x = client.list_tasks(cluster="phenomics-affinity-fleet")
        tasks = x['taskArns']
        tasks_defs = client.describe_tasks(
            cluster="phenomics-affinity-fleet",
            tasks=tasks
        )

        affinity_task_arn = ""
        affinity_port = ""

        for task_def in tasks_defs['tasks']:
            try:
                host_port = (task_def['containers'][0]['networkBindings'][0]['hostPort'])
                name_arn = task_def['taskDefinitionArn']
                name = cluster.find_name(name_arn)
                task_arn = task_def['taskArn']

                if name == 'phenomics-affinity-task-worker' + str(worker_id):
                    affinity_task_arn = task_arn
                    affinity_port = host_port

            except:
                logger.info("exception in task:".format(task_def))

        logger.info("Affinity Worker to be deleted: {}:{}:{}".format(worker_id, affinity_port, affinity_task_arn))
        response = client.stop_task(
            cluster="phenomics-affinity-fleet",
            task=affinity_task_arn,
            reason='Not working actively'
        )
        logger.info("Affinity worker deleted: {}".format(worker_id))
        return "{}".format(affinity_port)
