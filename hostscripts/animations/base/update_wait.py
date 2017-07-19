
from time import time


class Update_wait:
    """ base class for class that only update when a certain time has passed"""

    # test injection point
    get_time = time

    def __init__(self, update_every=1):
        self.update_every = update_every
        self.last_updated = -update_every - 1

    def iftimeout(self, set_last_update=True):
        """ return True/False base on if enough time has passed
            calling this mehtod also overwrite last_updated with current time
            flag False otherwise"""
        t = self.get_time()
        rlt = True if t - self.last_updated > self.update_every else False
        if set_last_update and rlt:
            self.last_updated = t

        return rlt
