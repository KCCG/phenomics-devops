from config_model import worker_config
def run():
    for x in range(0,8):
        record = worker_config.get_record(str(x))
        if record is not 0:
            # record.pipelinePort = str(9000 + x)
            record.isActive = 1
            record.save()

run()