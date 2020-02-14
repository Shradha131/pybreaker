class RingBuffer:

    def __init__(self, size_max):
        self.size = size_max
        self.data = []
        self.__class__ = RingBuffer

    class _Full:


        def clear(self):
            del self.data[:]

        def append(self, element):
            self.data[self.curr] = element
            self.curr = (self.curr + 1) % self.size
            self.old = self.data[self.curr]

        def get(self):
            return self.data

        def get_old_value(self):
            return self.old


    def append(self, element):
        self.data.append(element)
        if len(self.data) == self.size:
            self.curr = 0
            self.old = self.data[self.curr]
            self.__class__ = self._Full

    def get(self):
        return self.data
