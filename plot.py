import csv
from matplotlib.pyplot import plot,show

nums = []
with open('graph1.csv','rb') as csvfile:
    vals = csv.reader(csvfile,delimiter=',',quotechar='"')
    for row in vals:
        nums.append(map(float,row))
plot (nums[0],nums[1])
show()
