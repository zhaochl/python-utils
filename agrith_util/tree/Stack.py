#!/usr/bin/env python
# coding=utf-8
"""
Stack() 建立一个空的栈对象
push() 把一个元素添加到栈的最顶层
pop() 删除栈最顶层的元素，并返回这个元素
peek() 返回最顶层的元素，并不删除它
isEmpty() 判断栈是否为空
size() 返回栈中元素的个数
"""
class Stack:
    """模拟栈"""
    def __init__(self):
        self.items = []
       
    def isEmpty(self):
        return len(self.items)==0
   
    def push(self, item):
        self.items.append(item)
   
    def pop(self):
        return self.items.pop()
   
    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]
       
    def size(self):
        return len(self.items)
    def show(self):
        """
        print '*'*10+'print Stack start'+'*'*10
        for r in self.items:
            print r
        print '*'*10+'print Stack end'+'*'*10
        """
        print self.items
    def build_list(self):
        _results = []
        for r in self.items:
            _results.append(r)
        return _results
    def contains(self,item):
        _result = None
        if item in self.items:
            _result = True
        else:
            _result= False
        return _result
    def data(self):
        return self.items
if __name__ =='__main__':
    s=Stack()
    print(s.isEmpty())
    s.push(4)
    s.push('dog')
    print(s.peek())
    s.push(True)
    print(s.size())
    print(s.isEmpty())
    s.push(8.4)
    print(s.pop())
    print(s.pop())
    print(s.size())
