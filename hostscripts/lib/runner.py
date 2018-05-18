
class Runner:
    def __init__(self):
        self.modules = []

    def update(self):
        """ call update on all modules in run list"""
        for m in self.modules:
            m.update()

    def add_module(self, module_object):
        """ add module object into run list"""
        self.modules.append(module_object)

