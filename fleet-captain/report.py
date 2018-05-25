

class report:
    worker_id = 0
    busy_time = 0
    last_id = 0
    is_active = True
    is_healthy = True
    terminating = False
    port = 0
    def __init__(self, wid, btime, lid, iactive ,ihealthy):
        self.worker_id = wid
        self.busy_time = btime
        self.is_active = iactive
        self.last_id = lid
        self.is_healthy = ihealthy



    def __str__(self):

       if self.terminating:
           return "<tr style=\"color: #FF0000;\"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}({})<tr>".format(self.worker_id, self.busy_time, self.last_id,  self.is_active, self.is_healthy, self.terminating, self.port);

       if self.is_healthy:
            return "<tr style=\"color: #339933;\"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}<tr>".format(self.worker_id, self.busy_time,  self.last_id, self.is_active,self.is_healthy, self.terminating);
       else:
           return "<tr style=\"color: #cccc00;\"><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}<tr>".format(self.worker_id, self.busy_time, self.last_id,  self.is_active, self.is_healthy, self.terminating);

