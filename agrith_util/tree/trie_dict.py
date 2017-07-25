#!/usr/bin/env python
# coding=utf-8

class TrieTree(object):

  def __init__(self):
    self.tree = {}

  def add(self, word):
    tree = self.tree

    for char in word:
      if char in tree:
        tree = tree[char]
      else:
        tree[char] = {}
        tree = tree[char]

    tree['exist'] = True

  def search(self, word):
    tree = self.tree

    for char in word:
      if char in tree:
        tree = tree[char]
      else:
        return False

    if "exist" in tree and tree["exist"] == True:
      return True
    else:
      return False

tree = TrieTree()
tree.add("abc")
tree.add("bcd")
print(tree.tree)
# Print {'a': {'b': {'c': {'exist': True}}}, 'b': {'c': {'d': {'exist': True}}}}
print(tree.search("ab"))
# Print False
print(tree.search("abc"))
# Print True
print(tree.search("abcd"))
# Print False
