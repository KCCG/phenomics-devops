from cluster import cluster


def kill_all():
    order = input("Are you sure to kill the fleet?")
    if(order=='y'):
        for x in range(0,8):
            print ("Calling kill shot for worker:{}".format(x))
            cluster.delete_tasks(str(x))


kill_all()