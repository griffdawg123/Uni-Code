#!/usr/bin/python3

# from itertools import product
import numpy as np
import statistics
import sys

nums = [int(arg) for arg in sys.argv[1:]]
print(f"count={len(nums)}")
print(f"unique={len(set(nums))}")
print(f"minimum={min(nums)}")
print(f"maximum={max(nums)}")
print(f"mean={statistics.mean(nums)}")
print(f"median={statistics.median(nums)}")
print(f"mode={statistics.mode(nums)}")
print(f"sum={sum(nums)}")
print(f"product={np.prod(nums)}")
