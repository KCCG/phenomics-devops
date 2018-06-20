import boto3
import sys


def find_name(arn):
    index = arn.rfind('/')
    name = arn[index + 1: len(arn)]
    splits = name.split(':')
    return splits[0]


def delete_tasks(service_name, env):
    cluster_name = "phenomics-" + env

    print("Deploying:{} for Environment:{}".format(service_name, env))

    client = boto3.client('ecs')
    x = client.list_tasks(cluster=cluster_name)
    tasks = x['taskArns']

    if len(tasks) > 0:
        tasks_defs = client.describe_tasks(
            cluster=cluster_name,
            tasks=tasks
        )

        for task_def in tasks_defs['tasks']:
            try:
                host_port = (task_def['containers'][0]['networkBindings'][0]['hostPort'])
                name_arn = task_def['taskDefinitionArn']
                name = find_name(name_arn)
                task_arn = task_def['taskArn']

                if service_name in name:
                    print("Found task for the service. Cluster:{} | Task:{} | Port:{} ".format(cluster_name, task_arn,
                                                                                               host_port))
                    print("Deleting service task. ")
                    response = client.stop_task(
                        cluster=cluster_name,
                        task=task_arn,
                        reason='Deploying new container.'
                    )
                    print("Service task deleted: {}".format(task_arn))
                    return
            except:
                print("exception in task:".format(task_def))


if __name__ == "__main__":
    # service_name = sys.argv[1]
    # env = sys.argv[2]
    # delete_tasks(service_name, env)

    delete_tasks("test", "dev")
