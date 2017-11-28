
class Device:
    """ base class for device"""

    disable_flag = False

    def disable(self):
        """ disable and clean up divice 
            overwirte this method in sub class """
        raise NotImplemented("no implementation")

    def enable(self):
        """ re-enable device
            overwirte this method in sub class """
        raise NotImplemented("no implementation")
