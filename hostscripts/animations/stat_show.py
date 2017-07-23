from .base.update_wait import Update_wait
from itertools import cycle


class Stat_show(Update_wait):
    def __init__(self, slides, update_every=5):
        super().__init__(update_every)
        self.slides = cycle(slides)
        self.current_slide = None

    def update(self):
        if self.iftimeout():
            self.current_slide = next(self.slides)
        self.current_slide.show()


class Slide:
    """ should cantain two stats (two rows) """
    def __init__(self, lcd, stats):
        self.lcd = lcd
        self.stats = stats

    def show(self):
        for s in self.stats:
            data = s.get_data()
            if data is not None:
                self.lcd.setCursor(s.col, s.row)
                # TODO investgate why using 2 print does not work
                # head = "{}: ".format(s.name)
                # self.lcd.print(head)
                # ctn = str(data)
                # self.lcd.print(head + ctn)

                ctn = "{}: {}".format(s.name, data)
                ctnpad = ctn.ljust(s.space_padding, " ")
                self.lcd.print(ctnpad)


class _Stat(Update_wait):
    """ each stat takes 1 row by default """
    def __init__(self,
                 name,
                 update_every,
                 data_function,
                 row,
                 col,
                 space_padding=16):
        super().__init__(update_every)
        self.name = name
        self.data_function = data_function
        self.row = row
        self.col = col
        self.space_padding = space_padding
        self.last_data = None

    def get_data(self):
        """ return data, or None if no update"""
        if self.iftimeout():
            new_data = self.data_function()
            if new_data != self.last_data:
                return new_data
        return None


def single_slide(name1, data_function1, name2, data_function2, lcd):
    s1 = _Stat(name1, 5, data_function1, 0, 0)
    s2 = _Stat(name2, 5, data_function2, 1, 0)
    return Slide(lcd, [s1, s2])


def get_slides(lcd, name_function_tuple, update_every=5):
    l = int(len(name_function_tuple) / 2)
    it = iter(name_function_tuple)
    stats = [single_slide(*next(it), *next(it), lcd) for _ in range(l)]
    return Stat_show(stats, update_every)
