"""
class for notification led
"""

class Notification_led:
    def __init__(self, dev):
        self.dev = dev
        self.last_led_state = None

    def set_led(self, state):
        """set the state of the led 1/0"""
        if state != self.last_led_state:
            cmd = "{}{};".format(chr(75), chr(state))
            self.dev.write(cmd.encode())
            self.last_led_state = state

    def on(self):
        self.set_led(1)

    def off(self):
        self.set_led(0)
