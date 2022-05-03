import time

'''
sample = [1, 3, 15, 35, 34, 23, 1, 3, 5, 3, 7, 456, 2, 3, 223, 14, 21, 76, 66, 464, 32, 12, 125, 56, 34]

#버블 정렬_시간 복잡도 : O(N^2)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1, -1, -1):
        for j in range(0, i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                
    return arr


start = time.time()
print("Bubble Sort : ", bubble_sort(sample))
end = time.time()
print("The time of execution : ", end-start)

'''
import time

sample = [1, 3, 15, 35, 34, 23, 1, 3, 5, 3, 7, 456, 2, 3, 223, 14, 21, 76, 66, 464, 32, 12, 125, 56, 34]

#퀵 정렬_시간 복잡도 : O(NlogN)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    temp = arr[len(arr) // 2]
    left, equal, right = [], [], []
    for num in arr:
        if num < temp:
            left.append(num)
        elif num > temp:
            right.append(num)
        else:
            equal.append(num)
            
    return quick_sort(left) + equal + quick_sort(right)

start = time.time()
print("Quick Sort : ",quick_sort(sample))
end = time.time()
print("The time of execution : ", end-start)
            







