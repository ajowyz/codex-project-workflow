class ReadingList:
    def __init__(self):
        self._items = []

    def add(self, url):
        self._items.append(url)

    def items(self):
        return list(self._items)
