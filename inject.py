import random
import numpy as np
import pandas as pd

filepath=input("Filepath:")
probability=np.double(input("Probability of injection:"))
raw_data = pd.read_csv(filepath)
data=raw_data['Col3']
mode=int(input("MV(1) or Outlier(2)"))



dirty_data=[]
for i in range(0,len(raw_data)):
    if(random.uniform(0,1)>probability):
        print(i,data[i])
        dirty_data.append(data[i])
        break
    elif(mode==1):
        dirty_data.append(np.NaN)
    elif(mode==2):
        offset=random.uniform(-0.5,0.5)*data[i]
        dirty_data.append(data+offset)
    print("injection", i)

raw_data['Col3']=dirty_data


#file=open(input("Output:"))
raw_data.to_csv(input("Output file:"))