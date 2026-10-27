class Contact:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=10):
        if type(size) is not int or size <= 0:
            raise ValueError("Size must be a positive integer.")

        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        if not isinstance(key, str):
            raise TypeError("Contact names must be strings.")

        index = 0
        for character in key:
            index = (index * 31 + ord(character)) % self.size

        return index

    def insert(self, key, value):
        index = self.hash_function(key)

        if not isinstance(value, str):
            raise TypeError("Phone numbers must be strings.")

        current = self.data[index]

        # Update an existing contact instead of adding a duplicate.
        while current is not None:
            if current.key == key:
                current.value.number = value
                return

            current = current.next

        # Add a new contact at the beginning of this bucket's chain.
        new_node = Node(key, Contact(key, value))
        new_node.next = self.data[index]
        self.data[index] = new_node

    def search(self, key):
        current = self.data[self.hash_function(key)]

        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        return None

    def print_table(self):
        for index, head in enumerate(self.data):
            print(f"Index {index}:", end="")

            if head is None:
                print(" Empty")
                continue

            current = head

            while current is not None:
                print(f" - {current.value}", end="")
                current = current.next

            print()


def run_tests():
    # Contact formatting and Node attributes
    contact = Contact("Riley", "123-456-7890")
    assert str(contact) == "Riley: 123-456-7890"

    node = Node(contact.name, contact)
    assert node.key == "Riley"
    assert node.value is contact
    assert node.next is None

    # Empty table
    table = HashTable(10)
    assert len(table.data) == 10
    assert table.search("Chris") is None
    table.print_table()

    # Insert and retrieve contacts
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")

    assert table.search("John").number == "909-876-1234"

    # Update an existing number
    table.insert("Rebecca", "999-444-9999")
    assert table.search("Rebecca").number == "999-444-9999"

    # Missing contact
    assert table.search("Chris") is None

    # A one-bucket table guarantees collisions.
    collisions = HashTable(1)

    for name, number in [
        ("Amy", "111"),
        ("May", "222"),
        ("Sam", "333")
    ]:
        collisions.insert(name, number)

    for name, number in [
        ("Amy", "111"),
        ("May", "222"),
        ("Sam", "333")
    ]:
        assert collisions.search(name).number == number

    # Update the head, middle, and tail without adding duplicate nodes.
    for name in ("Sam", "May", "Amy"):
        collisions.insert(name, "999")
        assert collisions.search(name).number == "999"

    count = 0
    current = collisions.data[0]

    while current is not None:
        count += 1
        current = current.next

    assert count == 3
    assert collisions.search("Missing") is None

    # Invalid table sizes
    for invalid in (0, -1, 2.5, True):
        try:
            HashTable(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid size should raise ValueError."
            )

    print("\nUpdated contact table:")
    table.print_table()

    print("\nCollision test table:")
    collisions.print_table()

    print("\nAll hash table tests passed.")


if __name__ == "__main__":
    run_tests()


# DESIGN MEMO
#
# A hash table fits this contact manager because the main task is finding a
# phone number from a name. My hash function reads each character and combines
# its numeric value with the previous result, then uses the table size to keep
# the index within the array. This considers character order rather than only
# adding character values. The program searches the linked list at that index
# instead of checking every contact in the table.
#
# I handled collisions using separate chaining. Each array position holds the
# first node of a linked list. If different names reach the same index, they
# share that chain. Insertion checks the chain for an existing name first. If
# it finds one, it updates the phone number without adding another node. If the
# name is new, a node is added at the front of the chain. Searching follows
# these links until it finds the name or reaches None. Names are case-sensitive.
#
# An engineer might choose a hash table for contact directories, caches, or
# account lookups when exact matching matters more than sorted order. With
# short keys and a controlled load factor, lookup and insertion are O(1) on
# average. Hashing itself takes O(L) for a name of length L. Long chains can
# make operations O(n) for short keys, so a fixed-size table becomes slower as
# more contacts are added. A larger table or resizing would improve this at a
# memory cost. A list is simpler for small collections, while a balanced search
# tree is better when sorted traversal or range searches are needed.
