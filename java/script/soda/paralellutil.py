from .feedback import *
from queue import Queue
from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks, name):
        Thread.__init__(self)
        self.name = name
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(error(e))
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, name_of_workers):
        self._names = name_of_workers
        maxlength = len(max(name_of_workers,key=lambda n: len(n)))
        self.tasks = Queue(len(name_of_workers))
        for name in name_of_workers:
            Worker(self.tasks, name.ljust(maxlength))

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()