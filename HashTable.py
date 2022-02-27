# noinspection PyTypeChecker
# Hashtable file, used to speed up lookup times.
class HashTable:

    print("Hashtable starting")


    # A simple HashTable Constructor.
    # O(1) is both the space and time complexity.
    def __init__(self, size:int=100 ) -> None:
        # initialize the hash table with empty bucket list entries.
        self.map = [None] * size


    # A private getter to create or return truckDeliveryList hash key
    # O(1) is both the space and time complexity.
    def _getHash(self, key) :
        return int(key) % len(self.map)

    # Adds a new package value into the hash table
    # O(N) is both the space and time complexity.
    def add(self, key, value):
        keyHash = self._getHash(key)
        keyValue = [key, value]

        if self.map[keyHash] is None:
            self.map[keyHash] = list([keyValue])
            return True
        else:
            for item in self.map[keyHash]:
                if item[0] == key:
                    item[1] = keyValue
                    return True
            self.map[keyHash].append(keyValue)
            return True

    # Modifies a value in the hash table
    # O(N) is the space complexity. O(1) is the time complexity.
    def modify(self, key, value):
        keyHash = self._getHash(key)
        if self.map[keyHash] is not None:
            for item in self.map[keyHash]:
                if item[0] == key:
                    item[1] = value
                    return True


    # Reads a value from the hash table
    # O(N) is both the space and time complexity.
    def read(self, key):
        keyHash = self._getHash(key)
        if self.map[keyHash] is not None:
            for item in self.map[keyHash]:
                if item[0] == key:
                    return item[1]
        return None

    # Removes a value from the hash table
    # O(N) is both the space and time complexity.
    def remove(self, key):
        keyHash = self._getHash(key)

        if self.map[keyHash] is None:
            return False

        for item in len(self.map[keyHash]):
            if self.map[keyHash][item][0] == key:
                self.map[keyHash].pop(item)
                return True
        return False