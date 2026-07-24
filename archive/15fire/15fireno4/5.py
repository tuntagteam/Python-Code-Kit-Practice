import numpy as np

grades = np.array([60, 72, 85, 90, 68, 75, 88, 92, 55, 80])

mean = np.mean(grades)
median = np.median(grades)
std_dev = np.std(grades)
rangegrade = np.max(grades) - np.min(grades)

print(f"Mean: {mean}")
print(f"Median: {median}")
print(f"Standard Deviation: {std_dev:.2f}")
print(f"Range: {rangegrade}")
