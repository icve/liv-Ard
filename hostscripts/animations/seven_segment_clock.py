
from time import strftime
from .base.update_wait import Update_wait


class Seven_segment_clock(Update_wait):
    def __init__(self, ss_dev, sep="-", fmt=None, update_every=1):
        self.ss_dev = ss_dev
        self.sep = sep
        # entry point for testing
        self.strftime = strftime
        self.fmt = "%H{}%M{}%S".format(*(sep * 2)) if not fmt else fmt
        super().__init__(update_every) 

    def update(self):
        if not self.iftimeout():
            return
        for i, char in enumerate(reversed(self.get_fm_time())):
            self.ss_dev.write(char, i)

    def get_fm_time(self):
        return self.strftime(self.fmt)
