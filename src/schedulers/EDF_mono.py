from simso.core import Scheduler
from simso.core.Job import Job
from simso.core.Processor import Processor

class EDF_mono(Scheduler):
    # called when simulation is ready to start
    def init(self):
        self.ready_list = []

    # on task activation
    def on_activate(self, job: Job):
        self.ready_list.append(job)
        job.cpu.resched() # call the scheduler

    def on_terminated(self, job: Job):
        self.ready_list.remove(job)
        job.cpu.resched() # call the scheduler

    # called by the processor when it needs to run the scheduler
    def schedule(self, cpu: Processor):
        if self.ready_list:  # If at least one job is ready:
            # job with the highest priority
            job: Job = min(self.ready_list, key=lambda x: x.absolute_deadline)
        else:
            job = None

        return (job, cpu)
