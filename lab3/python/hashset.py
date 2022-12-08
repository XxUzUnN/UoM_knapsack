from enum import Enum
import config


class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.hash_value = None
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.hash_table = [None] * self.hash_table_size
        self.access = 0
        self.rehash = 0

    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 1
        return True

    def nextPrime(self, n):
        while not self.isPrime(n):
            n = n + 1
        return n

    def hashValue(self, value):
        if self.mode == 0 or self.mode == 1 or self.mode == 2:
            sum = 0
            for letter in value:
                sum = sum + ord(letter) ** 2
            return (3 * sum + 7) % self.hash_table_size
        elif self.mode == 4 or self.mode == 5 or self.mode == 6:
            sum = 0
            for letter in value:
                sum = sum + ord(letter) ** 3
            return (sum ** 3) % self.hash_table_size

    def hashValue2(self, value):
        if self.mode == 2:
            sum = 0
            for letter in value:
                sum = sum + ord(letter) ** 2
            return (3 * sum + 7) ** 3 % self.hash_table_size
        elif self.mode == 6:
            sum = 0
            for letter in value:
                sum = sum + ord(letter) ** 3
            return (sum ** 3) ** 3 % self.hash_table_size

    def insert_linear(self, value):
        hash_value = self.hashValue(value)
        for i in range(hash_value, self.hash_table_size):
            if self.hash_table[i] is None:
                self.hash_table[i] = value
                return True
            elif self.hash_table[i] == value:
                return False
        for i in range(0, hash_value):
            if self.hash_table[i] is None:
                self.hash_table[i] = value
                return True
            elif self.hash_table[i] == value:
                return False
        self.resize()
        self.insert(value)

    def insert_quadratic(self, value):
        hash_value = self.hashValue(value)
        for i in range(0, self.hash_table_size):
            position = (hash_value + i * i) % self.hash_table_size
            if self.hash_table[position] == value:
                return False
            elif self.hash_table[position] is None:
                self.hash_table[position] = value
                return True
        self.resize()
        self.insert(value)

    def insert_double(self, value):
        hash_value1 = self.hashValue(value)
        for i in range(0, self.hash_table_size):
            hash_value2 = self.hashValue2(value)
            position = (hash_value1 + i * hash_value2) % self.hash_table_size
            if self.hash_table[position] == value:
                return False
            elif self.hash_table[position] is None:
                self.hash_table[position] = value
                return True
        self.resize()
        self.insert(value)

    def resize(self):
        self.hash_table_size = self.nextPrime(self.hash_table_size * 2)
        previous_hash_table = self.hash_table
        self.hash_table = [None] * self.hash_table_size
        for value in previous_hash_table:
            if value is not None:
                if self.mode == 0 or self.mode == 4:
                    if self.insert_linear(value):
                        self.rehash = self.rehash + 1
                elif self.mode == 1 or self.mode == 5:
                    if self.insert_quadratic(value):
                        self.rehash = self.rehash + 1
                elif self.mode == 2 or self.mode == 6:
                    if self.insert_double(value):
                        self.rehash = self.rehash + 1
                else:
                    print("Error: Unknown mode")

    def insert(self, value):
        # TODO code for inserting into  hash table
        if self.mode == 0 or self.mode == 4:
            if self.insert_linear(value) is True:
                self.access = self.access + 1
        elif self.mode == 1 or self.mode == 5:
            if self.insert_quadratic(value) is True:
                self.access = self.access + 1
        elif self.mode == 2 or self.mode == 6:
            if self.insert_double(value) is True:
                self.access = self.access + 1
        else:
            print("Error: Unknown mode")

    def find(self, value):
        # TODO code for looking up in hash table
        if self.mode == 0 or self.mode == 4:
            hash_value = self.hashValue(value)
            for i in range(hash_value, self.hash_table_size):
                if self.hash_table[i] == value:
                    return True
                elif self.hash_table[i] is None:
                    return False
            for i in range(0, hash_value):
                if self.hash_table[i] == value:
                    return True
                elif self.hash_table[i] is None:
                    return False
        elif self.mode == 1 or self.mode == 5:
            hash_value = self.hashValue(value)
            for i in range(0, self.hash_table_size):
                position = (hash_value + i * i) % self.hash_table_size
                if self.hash_table[position] is None:
                    return False
                elif self.hash_table[position] == value:
                    return True
            return False
        elif self.mode == 2 or self.mode == 6:
            hash_value1 = self.hashValue(value)
            for i in range(0, self.hash_table_size):
                hash_value2 = hash_value1 ** 3
                position = (hash_value1 + i * hash_value2) % self.hash_table_size
                if self.hash_table[position] is None:
                    return False
                elif self.hash_table[position] == value:
                    return True
            return False
        else:
            print("Error: Unknown mode")

    def print_set(self):
        # TODO code for printing hash table
        for i in range(0, self.hash_table_size):
            if self.hash_table[i] is not None:
                print(i, self.hash_table[i])

    def print_stats(self):
        # TODO code for printing statistics
        print("Mode:", self.mode)
        elements = 0
        collisions = 0
        for i in range(self.hash_table_size):
            if self.hash_table[i] is not None:
                elements = elements + 1
                if self.mode == 0 or self.mode == 4:
                    if self.hashValue(self.hash_table[i]) != i:
                        collisions = collisions + 1
                elif self.mode == 1 or self.mode == 5 or self.mode == 2 or self.mode == 6:
                    if self.hashValue(self.hash_table[i]) % self.hash_table_size != i:
                        collisions = collisions + 1
        print("Number of collisions:", collisions)
        print("Number of rehashed:", self.rehash)
        print("Number of accesses:", self.access)
        print("Average collisions per access:", collisions / self.access)


# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self):
        pass


class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2


# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING = 0
    HASH_1_QUADRATIC_PROBING = 1
    HASH_1_DOUBLE_HASHING = 2
    HASH_1_SEPARATE_CHAINING = 3
    HASH_2_LINEAR_PROBING = 4
    HASH_2_QUADRATIC_PROBING = 5
    HASH_2_DOUBLE_HASHING = 6
    HASH_2_SEPARATE_CHAINING = 7
