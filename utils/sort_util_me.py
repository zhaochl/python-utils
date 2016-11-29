#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
# 各种排序算法
# author zcl
# date：2016/1/11
#选择排序
def select_sort(sort_array,asc=True):
    for i, elem in enumerate(sort_array):
        for j, elem in enumerate(sort_array[i:len(sort_array)]):
            if asc:
                if sort_array[i] > sort_array[j + i]:
                    #交换
                    sort_array[i], sort_array[j + i] = sort_array[j + i], sort_array[i]
            else:
                if sort_array[i] < sort_array[j + i]:
                    #交换
                    sort_array[i], sort_array[j + i] = sort_array[j + i], sort_array[i]
    return sort_array

#冒泡排序
def bubble_sort(sort_array):
    for i, elem in enumerate(sort_array):
        for j, elem in enumerate(sort_array[:len(sort_array) - i - 1]):
            if sort_array[j] > sort_array[j + 1]:
                sort_array[j], sort_array[j + 1] = sort_array[j + 1], sort_array[j]
#插入排序
def insert_sort(sort_array):
    for i, elem in enumerate(sort_array):
        for j, elem in enumerate(sort_array[:i]):
            if sort_array[j] > sort_array[i]:
                sort_array.insert(j, sort_array[i])
                del sort_array[i + 1]
#归并排序
def merge_sort_wrapper(sort_array):
    merge_sort(sort_array, 0, len(sort_array) - 1)

def merge_sort(sort_array, left = 0, right = 0):
    if left < right:
        center = (left + right) / 2
        merge_sort(sort_array, left, center)
        merge_sort(sort_array, center + 1, right)
        merge(sort_array, left, right, center)

def merge(sort_array, left, right, center):
    result = []
    arrayA = sort_array[left:center + 1]
    arrayB = sort_array[center + 1:right + 1]
    while((len(arrayA) > 0) and (len(arrayB) > 0)):
        if(arrayA[0] > arrayB[0]):
            result.append(arrayB.pop(0))
        else:
            result.append(arrayA.pop(0))

    if(len(arrayA) > 0):
        result.extend(arrayA)
    if(len(arrayB) > 0):
        result.extend(arrayB)   
    sort_array[left:right + 1] = result
#快排    
def quick_sort(sort_array):
    if(len(sort_array) < 2):
        return

    left = [x for x in sort_array[1:] if x < sort_array[0]]
    right = [x for x in sort_array[1:] if x >= sort_array[0]]
    quick_sort(left)
    quick_sort(right)
    sort_array[:] = left + [sort_array[0]] + right

#shell排序
def shell_sort(sort_array):
    dist=len(sort_array)/2  
    while dist > 0:  
        for i in range(dist,len(sort_array)):  
            tmp=sort_array[i]  
            j = i  
            while j >= dist and tmp < sort_array[j - dist]:  
                sort_array[j] = sort_array[j - dist]  
                j -= dist  
            sort_array[j] = tmp  
        dist /= 2  

#基数排序,均为整数，不支持负数和重复
def radix_sort(sort_array):
    max_elem = max(sort_array)
    bucket_list = []
    for i in range(max_elem):
        bucket_list.insert(i, 0)

    for x in sort_array:
        bucket_list[x - 1] = -1

    sort_array[:] = [x + 1 for x in range(len(bucket_list)) if bucket_list[x] == -1]
#堆排序
def heap_sort(sort_array):
   #没有写出来，再想想
   pass
#测试例子
def algo_sort_test(sort_array, sort_method):
    sort_method(sort_array)

if __name__ == '__main__':
    print '---------select_sort-asc----'
    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    select_sort(sort_array,True)
    print sort_array
    print '---------select_sort-desc----'
    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    select_sort(sort_array,False)
    print sort_array
    print '---------bubble_sort-desc----'
    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    algo_sort_test(sort_array, bubble_sort)
    print sort_array    

    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    algo_sort_test(sort_array, insert_sort)
    print sort_array      

    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    algo_sort_test(sort_array, merge_sort_wrapper)
    print sort_array

    sort_array = [1, 2, 3, 5, -4, 4, 10, 300, 19, 13, 16, 18, 500, 190, 456, 23]
    algo_sort_test(sort_array, quick_sort)
    print sort_array 
    sort_array = [1, 2, 3, 5, -4, 4, 10, 3, 19, 13, 16, 18, 5, 190, 456, 23]
    algo_sort_test(sort_array, shell_sort)
    print sort_array       

    sort_array = [1, 2, 3, 5, 4, 10, 19, 13, 16, 18, 190, 456, 23]
    algo_sort_test(sort_array, radix_sort)
    print sort_array       

    print 'OK'
