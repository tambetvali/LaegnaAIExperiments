# Quanda - Flashcard, Question and Answer card (from Q'n'A without special chars)

"""
  SimpleQuanda

  Add Q&A nodes, and associate their structure based on parent with Anytree.
  - Use Anytree for efficient traversal of the result.

  This can be used to organize converstations into tree-like structure of Q&A cards, with queries
  of Anytree: Anytree keeps track of all node relations, given the parent of each node.
"""

import anytree

class SimpleQuandaOracle:
    def __init__(self, child = None):
        if child != None:
          self.child = child
          self.counttofuture = child.counttofuture + 1
        else:
          self.counttofuture = 0
    
    # Oracle knows it's *distance from the future*
    def __str__(self):
        return str(self.counttofuture)

# Works best for one thread or calm threading
class SimpleQuanda:
    def __init__(self, question, parent = None, mockanswer = None):
        # Parent quanda
        self.node = anytree.Node(str(id(self)), quandainst=self)
        self.parent = parent # including None to avoid "no attribute" errors
        if parent != None: # must be other quanda
            self.node.parent = parent.node
        # We have the question
        self.Q = question
        # We have mock answer: it pretends that AI answered this
        # - we do not connect real AI models for snippet code.
        self.mA = mockanswer
        self.lazy = True
    
    def ask(self, question, mockanswer = None):
        # Answer is new quanda instance; set self as parent and provide mock answer
        # - mock answer is emulated to play an AI model call
        return SimpleQuanda(question, self, mockanswer)
    
    # AI call should be implemented here, yielding pieces
    # - streaming string methods should operate on call
    # - inherited class could hide this and create HTML element instead
    def __call__(self):
        # If answer is there
        if self.lazy == False:
            # Still emulate streaming
            yield self.A
            return

        # Yield your own messages at the end

        # This will be filled with chars
        answer = ""

        # Just yield the mock answer char by char
        for char in self.mA:
            answer += char
            yield char

        # Store the result
        self.A = answer
    
    def messages(self, self_oracle = None):
        if self_oracle == None:
            # The oracle of the last node just contains itself
            self_oracle = SimpleQuandaOracle()

        # Recursively call parent messages
        if self.parent != None:
            # The oracle of parent not not just contains youself, but also links to the parent
            # - indeed, this simple oracle only contains count to the future, nothing more.
            for msg in self.parent.messages(SimpleQuandaOracle(self_oracle)):
                yield msg
        
        # TODO: if oracle step count is more than 3, you could summarize the message for future watcher.
        #       - use clever compression strategies and summarization pool.

        # Normally, these would be converted to role and content, but we have very simplistic display.
        yield { "Q": self.Q, "@": str(self_oracle) }
        yield { "A": self.A, "@": str(self_oracle) }

    # Wait for answer so that "A" variable would appear - thus, use the loop once
    def wait(self):
        for a in self():
            pass

        # Still return the result
        return self.A
    
    # Whether it has associated the "A" attribute of answer
    def done(self):
        return hasattr(self, "A")

    # Wait and done: you could use them in getters for Q and A. Accessors, which won't support
    # streaming, would miss that syntax whatsoever.

    def __str__(self):
        return f"[ Q: {self.Q}, A: {self.A} ]"
    
    # From UserList

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__getslice__(i.start, i.stop)
        return self.node.path[i].quandainst

    def __getslice__(self, i, j):
        slic = []
        for nod in self.node.path[i:j]:
            slic.append(nod.quandainst)
        
        return slic
    
    def __len__(self):
        return len(self.node.path)


# When called as main script, first emulate one SimpleQuanda
if __name__ == "__main__":
    print("Unit test 1")
    print()

    # First question, and it's __call__ to calculate answer instantly.
    quanda1 = SimpleQuanda("What is my name?", None, "You are anonymous user.")
    quanda1.wait()
    print("Does it have an answer: ", quanda1.done())
    print(quanda1)

    # Second question, and it's __call__ to calculate answer instantly.
    quanda2 = quanda1.ask("What makes my user anonymous?", "My authentication service.")

    # A line feed
    print()

    # Stream the second message.
    # - If it only thinks it's streaming, it will stream it in one piece.
    # - the __call__ can only used for loops, which might be standard way to ask.
    print(f"Q: {quanda2.Q}")
    print("A: ", end="")
    for token in quanda2():
        print(token, end="")
    print()

    print()
    print()

    # Display the path of quanda2, which will give us the list of all Q&A pairs in it's conversation.
    print("Node path of second Quanda: ", quanda2.node.path)
    print()

    print("All ", len(quanda2), " path elements by names:")
    for node in quanda2.node.path:
        print(node.name)
    print()

    print("Second element in path")
    print(node.path[1].name)
    print("Same element as quanda object, not anytree's node")
    print(quanda2[1])
    print()

    print("Path elements from 0 to 1")
    print(node.path[0:2])
    for el in quanda2[0:2]:
        print(el)
    print()

    for msgo in quanda2.messages():
        print(msgo)