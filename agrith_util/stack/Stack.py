#coding:utf-8
#author:Elvis

class Stack(object):

  def __init__(self, size=8):
    self.stack = []
    self.size = size
    self.top = -1

  def is_empty(self):
    if self.top == -1:
      return True
    else:
      return False

  def is_full(self):
    if self.top +1 == self.size:
      return True
    else:
      return False

  def push(self, data):
    if self.is_full():
      raise Exception('stackOverFlow')
    else:
      self.top += 1
      self.stack.append(data)

  def stack_pop(self):
    if self.is_empty():
      raise Exception('stackIsEmpty')
    else:
      self.top -= 1
      return self.stack.pop()


  def stack_top(self):
    if self.is_empty():
      raise Exception('stackIsEmpty')
    else:
      return self.stack[self.top]

  def show(self):
    print self.stack

stack = Stack()
stack.push(1)
stack.push(2)
stack.push('a')
stack.push('b')
stack.push(5)
stack.push(6)
stack.stack_pop()
stack.stack_pop()
stack.stack_top()
stack.is_empty()
stack.is_full()
stack.show()