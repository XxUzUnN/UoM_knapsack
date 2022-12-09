import config


class bstree:
    def __init__(self):
        self.verbose = config.verbose
        self.insert_access = 0
        self.find_access = 0

    def size(self):
        if self.tree():
            return 1 + self.left.size() + self.right.size()
        return 0

    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def insert(self, value):
        self.insert_access = self.insert_access + 1
        if self.tree() is True:
            # TODO if tree is not NULL then insert into the correct sub-tree
            if value < self.value:
                self.left.insert(value)
            elif value > self.value:
                self.right.insert(value)
        else:
            # TODO otherwise create a new node containing the value
            self.value = value
            self.left = bstree()
            self.right = bstree()

    def find(self, value):
        self.find_access = self.find_access + 1
        if self.tree():
            # TODO complete the find function
            if value < self.value:
                return self.left.find(value)
            elif value > self.value:
                return self.right.find(value)
            else:
                return True
        else:
            return False

    def height(self):
        if self.tree() is True:
            return 1 + max(self.left.height(), self.right.height())
        return 0

    def insertNum(self):
        if self.tree():
            return self.insert_access + self.left.insertNum() + self.right.insertNum()
        return self.insert_access

    def findNum(self):
        if self.tree():
            return self.find_access + self.left.findNum() + self.right.findNum()
        return self.find_access

    # You can update this if you want
    def print_set_recursive(self, depth):
        if self.tree():
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)

    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)

    def print_stats(self):
        # TODO update code to record and print statistic
        if self.tree():
            print("BSTree size:", self.size())
            print("BSTree height:", self.height())
            print("BSTree average insert:", self.insert_access / self.size())
            print("BSTree average find:", self.find_access / self.size())
        else:
            print("BSTree is empty")
