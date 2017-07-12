import time


class Seven_segment_clock():
    def __init__(self, ss_dev, sep="-", fmt=None):
        self.ss_dev = ss_dev
        self.sep = sep
        # entry point for testing
        self.time = time
        self.fmt = "%H{}%M{}%S".format(*(sep * 2)) if not fmt else fmt

    def update(self):
        for i, char in enumerate(reversed(self.get_time())):
            self.ss_dev.write(char, i)

    def get_time(self):
        return self.time.strftime(self.fmt)
