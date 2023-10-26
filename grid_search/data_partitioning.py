import math
import doctest
import numpy as np


range = np.arange

def l_mul(l_nums):
    result = 1
    for i in l_nums:
      result *= i
    return result

def num_of_elements_in(start, end, range):
  '''
  >>> num_of_elements_in(10, 100, 1) - len(range(10,100,1))
  0
  
  >>> num_of_elements_in(20, 500, 3) - len(range(20, 500, 3))
  0
  '''
  return math.ceil((end - start) / range)

interval = [
    [1.3, 14.5, 2.2],
    [11.3, 15+np.pi, np.pi**2-1],
    [21, 30, 3]
  ]

max_batch_items = 100

# we want to divide the interval into N intervals with a maximum of max_batch_items each

paramsN = len(interval)

total_elements = l_mul(num_of_elements_in(*p) for p in interval)
min_batches = total_elements // max_batch_items + 1
currentBatches = 1


def calc_partitions(interval, min_partitions, paramsN):
  partitions = [ 1 for i in range(paramsN) ]
  partitions_n = lambda: l_mul(partitions)
  partitions_m = lambda: math.ceil(min_partitions / partitions_n())
  
  for param_num in range(paramsN):
    missing_partitions = partitions_m()
    
    elements = num_of_elements_in(*interval[param_num])
    if elements > missing_partitions:
      partitions[param_num] *= missing_partitions
      break
    else:
      partitions[param_num] *= elements
    
  return partitions


partitions = calc_partitions(interval, min_batches, paramsN)
current_partition = [ 0 for i in range(paramsN) ]
def next_partition():
  global partitions
  global current_partition
  
  if not current_partition:
    return None
  
  # calc current elements
  current_elements = [ [] for _ in range(paramsN) ]
  
  for i in range(paramsN):
    start, end, step = interval[i]
    elements = num_of_elements_in(start, end, 1)
    i_partitions = partitions[i]
    i_partition = current_partition[i]
    
    min_start = start + elements * i_partition / i_partitions
    i_start = start
    while i_start < min_start: i_start += step
      
    min_end = start + elements * (i_partition + 1) / i_partitions
    i_end = i_start
    while i_end < min_end: i_end += step
    if i_end > end: i_end = end
    
    current_elements[i] = [ i_start, i_end, step ]
    
  # calc next partition
  
  for i in range(paramsN):
    current_partition[i] += 1
    if current_partition[i] < partitions[i]:
      break
    
    current_partition[i] = 0
    if i == paramsN - 1:
      current_partition = None
    
  return current_elements
    

print("Interval:", interval , "(", total_elements, "elements )")
print("Max batch items:", max_batch_items)
print("Min batches:", min_batches)
print("Actual batches", l_mul(partitions))
print("Partitions:", partitions)

bench_results = []
for i in range(*interval[0]):
  for j in range(*interval[1]):
    for k in range(*interval[2]):
      bench_results.append((i, j, k))

test_results = []
while True:
  p = next_partition()
  print(p)
  if not p: break
  
  for i in range(*p[0]):
    for j in range(*p[1]):
      for k in range(*p[2]):
        test_results.append((i, j, k))

error = False

# compare results
for element in bench_results:
  try:
    test_results.remove(element)
  except ValueError:
    error = True
    print("Missing element:", element)
    
for element in test_results:
  error = True
  print("Unexpected element:", element)
  
if not error:
  print("Test passed")

doctest.testmod()
