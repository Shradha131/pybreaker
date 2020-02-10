class RingBuffer:

    def __init__(self, size_max):
        self.curr = 0
        self.size = size_max
        self.data = []
        self.__class__ = RingBuffer

    class _Full:
        def __init__(self):
            self.curr = 0
            self.old = 0
            self.new = 0

        def append(self, element):
            self.new = element
            self.old = self.data[self.curr]
            self.data[self.curr] = self.new
            self.curr = (self.curr + 1) % self.size

        def get(self):
            return self.data

        def get_old_value(self):
            return self.old

        def get_curr_value(self):
            return self.new

    def append(self, element):
        self.data.append(element)
        if len(self.data) == self.size:
            self.__class__ = self._Full

    def get(self):
        return self.data
