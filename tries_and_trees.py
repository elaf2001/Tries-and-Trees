# Elaf Abdullah Saleh Alhaddad (31063977)
# Assignment 3 - Task 1
class Node:
    """
    Class that is used to represent the node in the trie
    Attributes:
        - Frequency: the frequency of the highest reoccurring string
        - link: the link of the node to other nodes
        - index_next: assists in storing the next node letter of the most occurring string/ smallest lexicographically
        in case the frequency is the same
        - index: stores the letter of the node
        - highest_freq: stores the leaf of the string with highest frequency/ smallest lexicographically in case the
        frequency is the same
        - string: the key inputted in the database
    """

    def __init__(self, size=5):
        """
        Constructor for the Node class
        :param size: Five because the string input is limited [A-D] and $ for the termination
        """
        self.frequency = 0
        self.link = [None] * size  # Size 4 + 1: 4- stands for A,B,C,D and 1- stands for $
        self.index_next = 0
        self.highest_freq = None
        self.string = ""
        self.index = 0


# Assignment 3 - Task 1
class SequenceDatabase:
    """
    Represents the database
    Attributes:
        - root: the root of the trie
        - is_empty: True - the trie is empty, False - trie has Nodes inside
    """

    def __init__(self):
        """
        Constructor of SequenceDatabase
        """
        self.root = Node()
        self.is_empty = True

    def addSequence(self, key):
        """
        Responsible for adding the strings into the database
        :param key: the string that will be added to the database
        :Time complexity: O(N^2) - N is the length of the string key
        """
        self.is_empty = False
        current = self.root
        i = 0
        highest_leaf = self.addSequence_aux(current, key, i)
        # Updating the root
        # If it is the first element that is added to the database
        if highest_leaf.highest_freq is None:
            current.highest_freq = highest_leaf
            current.frequency = highest_leaf.frequency
            current.index_next = highest_leaf.index
        else:
            # Compare the frequency if it is not the first element on the database
            if current.frequency < highest_leaf.frequency:
                current.frequency = highest_leaf.frequency
                current.highest_freq = highest_leaf.highest_freq
                current.index_next = highest_leaf.index
            # If the frequency is equal then compare the lexicographical order
            elif current.frequency == highest_leaf.frequency:
                if current.index_next >= highest_leaf.index:
                    current.frequency = highest_leaf.frequency
                    current.highest_freq = highest_leaf.highest_freq
                    current.index_next = highest_leaf.index

    def addSequence_aux(self, current, key, i):
        """
        Called to assist in recursion of the process of adding strings to the database
        :param current: the node to process from - adding new node in case it doesn't exist
        :param key: the string that is added to the database
        :param i: the index of the key to process
        :return: the current node to be processed in recursion
        """
        # base
        if i == len(key):
            index = 0

            # Create leaf node
            prev = current
            if current.link[index] is not None:
                current = current.link[index]
            # If path doesn't exist
            else:
                current.link[index] = Node()
                current = current.link[index]
            current.frequency += 1
            current.string = key
            # If it is the first node added on database that ends with the prev letter
            if prev.highest_freq is None:
                prev.highest_freq = current
            # If it is not then compare it's frequency
            else:
                if prev.highest_freq.frequency < current.frequency:
                    prev.highest_freq = current
            return current
        elif i < len(key):
            # Calculate index
            # $ = 0, A = 1, B = 2, C = 3, D = 4
            index = ord(key[i]) - 65 + 1
            # If path exist
            if current.link[index] is not None:
                current = current.link[index]
            # If path doesn't exist
            else:
                current.link[index] = Node()
                current = current.link[index]
            i += 1

            # Increments the frequency of occurrence
            leaf = self.addSequence_aux(current, key, i)
            # Updating the element that is right before the end of the string
            if leaf.highest_freq is None:
                # If its the first element added to the database
                if current.highest_freq is None:
                    current.highest_freq = leaf
                    current.frequency = leaf.frequency
                    current.index_next = leaf.index
                    current.index = index
                # If its not the first element, compare to the frequency of the existing string of highest frequency
                else:
                    if current.frequency < leaf.frequency:
                        current.frequency = leaf.frequency
                        current.highest_freq = leaf
                        current.index_next = leaf.index
                        current.index = index
                    # if they have the same frequency then compare the lexicographical order
                    elif current.frequency == leaf.frequency:
                        if current.index_next >= leaf.index:
                            current.index_next = leaf.index
                            current.frequency = leaf.frequency
                            current.highest_freq = leaf
            else:
                # Updating the rest of the elements
                if current.frequency < leaf.frequency:
                    current.frequency = leaf.frequency
                    current.highest_freq = leaf.highest_freq
                    current.index_next = leaf.index
                    current.index = index
                # if they have the same frequency then compare the lexicographical order
                elif current.frequency == leaf.frequency:
                    if current.index_next >= leaf.index:
                        current.index_next = leaf.index
                        current.frequency = leaf.frequency
                        current.highest_freq = leaf.highest_freq
            return current

    def query(self, q):
        """
        Search for substring with highest occurring frequency that has q as prefix
        :param q: prefix of the substring
        :return:
            - a string that has q as prefix
            - should have higher frequency in the database than any other string with q as a prefix
            - if two or more strings with prefix q are tied for most frequent it will return the lexicographically least
            of them
            - None if no string exist
        """
        if self.is_empty:
            return None
        current = self.root
        i = 0
        while i < len(q):
            index = ord(q[i]) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
            else:
                return None
            i += 1
        return current.highest_freq.string


# Assignment 3 - Task 2
class Node_2:
    """
    Class that is used to represent the node in the trie
    Attributes:
        - link: the link of the node to other nodes
        - all_index: contains the index where the node occurs in the string
    """

    def __init__(self, size=5):
        """
        Constructor
        :param size: Five because the string input is limited [A-D] and $ for the termination
        """
        self.all_index = []
        self.link = [None] * size  # Size 4 + 1: 4- stands for A,B,C,D and 1- stands for $


class OrfFinder:
    """
    The class that will contain the suffix trie of the string
    Attributes:
        - root: the root of the trie
        - genome: the string to find the substrings in
    """

    def __init__(self, genome):
        """
        constructor for the suffix trie
        :time complexity: worst time complexity: O(N^2) - N is the length of genome
        :param genome: the string to find the substrings in
        """
        self.root = Node_2()
        self.genome = genome
        self.create_trie(genome)  # O(N^2)

    def create_trie(self, genome):
        """
        Creating the suffix trie
        :param genome: string to create the trie from
        :time complexity: O(N^2) - N is the length of the genome
        """
        i = 0
        while i <= len(genome):  # O(N)
            current = self.root
            self.create_trie_aux(current, genome, i)  # O(N)
            i += 1

    def create_trie_aux(self, current, key, i):
        """
        Called to assist in recursion of the process of creating the suffix
        :param current: the node to process from - adding new node in case it doesn't exist
        :param key: the string that is added to the database
        :param i: the index of the key to process
        :time complexity: O(N) - N is the length of key
        """
        if i > len(key):
            return
        else:
            # Calculate index
            # $ = 0, A = 1, B = 2, C=3, D=4
            if i == len(key):
                index = 0
            else:
                index = ord(key[i]) - 65 + 1
                data = key[i]
            # If path exist
            if current.link[index] is not None:
                current = current.link[index]
                current.all_index.append(i)

            # If path doesn't exist
            else:
                current.link[index] = Node_2()
                current = current.link[index]
                current.all_index.append(i)

            # Increments the frequency of occurrence
            i += 1
            # recur
            self.create_trie_aux(current, key, i)

    def find(self, start, end):
        """
        :param start: non-empty string consisting of only uppercase [A-D] - makes the prefix of the substring
        :param end: non-empty string consisting of only uppercase [A-D] - makes the suffix of the substring
        :return: list of strings:
            - substrings of genome which have start as prefix and end as suffix
        :time complexity: O(len(start) + len(end) + U)
            - U is O(1) when the substrings are not found
            - U is O(N^2) when the substrings are found - N is the length of genome
        """
        answers = []
        ans = ""
        # STARTING POINTS
        current = self.root
        for i in start:
            index = ord(i) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
                ans += self.genome[current.all_index[0]]
                starting_points = current.all_index
            else:
                starting_points = []

        # ENDING POINTS
        current = self.root
        for j in end:
            index = ord(j) - 65 + 1
            if current.link[index] is not None:
                current = current.link[index]
                ending_points = current.all_index
            else:
                ending_points = []

        for i in starting_points:
            for j in ending_points:
                # ensure that the start of the ending point is not the same as the end of the starting point
                if i < j and i < j + 1 - len(end):
                    ans += self.genome[i + 1:j + 1]
                    answers.append(ans)
                ans = start

        return answers
