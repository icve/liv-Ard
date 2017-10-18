import logging
from logging.handlers import RotatingFileHandler
from time import time


class Motion_sensor:

    def __init__(self,
                 dev,
                 log_path,
                 update_intv=1,
                 log_max_size=1e6,
                 backupCount=10):
        # set up logging
        logger = logging.getLogger("mtlog")
        handler = RotatingFileHandler(log_path,
                                      maxBytes=log_max_size,
                                      backupCount=backupCount)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt="%(asctime)s, %(message)s",
                                      datefmt="%d/%m/%y %X")
        handler.setFormatter(formatter)
        logger.info("Starting")
        self.logger = logger
        # allow for better testing
        self.get_time = time
        self.update_intv = update_intv
        self.dev = dev
        self.last_state = None
        # to ensure the first call of update method always work
        # the value of last_update must satisfy
        # i - last_update > update_intv where i >=0 
        self.last_update = -update_intv - 1
        self.last_led_state = None

    def update(self):
        diff = self.get_time() - self.last_update
        if (diff > self.update_intv):
            state = self.get_state()
            if state != self.last_state:
                self.logger.info(str(state))
                self.last_state = state
                self.set_led(state)

            self.last_update = self.get_time()

    def get_state(self):
        """return state of the motion sensor, 1/0"""
        cmd = "{};".format(chr(76)).encode()
        self.dev.write(cmd)
        return ord(self.dev.read(1))

    def set_led(self, state):
        """set the state of the led 1/0"""
        if state != self.last_led_state:
            cmd = "{}{};".format(chr(75), chr(state))
            self.dev.write(cmd.encode())
            self.last_led_state = state
