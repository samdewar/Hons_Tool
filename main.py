import csv
import math
import statistics
import tkinter.messagebox
from tkinter import *
#import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
import sklearn as sk
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import KNNImputer
from sklearn.mixture import GaussianMixture
from scipy.stats import t
import datetime
#import autoregression

global filepath
#global raw_data

def start_gui():
    win = Tk()  # creating the main window and storing the window object in 'win'
    win.title('Welcome')  # setting title of the window
    win.geometry('500x500')  # setting the size of the window
    def Read_File():
        global raw_data
        global data
        global temps
        global humids
        humids=[]
        temps=[]
        raw_data = pd.read_csv("output.csv")

        temp=raw_data['Temp']
        humid=raw_data['Humid']

        days=[]
        for i in range(0,len(raw_data)):
            temps.append(int(temp[i]))
            humids.append(int(humid[i]))

        #dt=datetime.datetime(raw_data['Day'],raw_data['Time'])
        data ={'Date-Time':days,'Temp':temp}
        data2 = sm.datasets.sunspots.load_pandas().data['SUNACTIVITY']


        print("Read File: ",filepath.get())
        return

    def Read_File_MV():
        global raw_data
        global data
        global temps
        temps=[]
        raw_data = pd.read_csv("output.csv")

        temp=raw_data['Temp']
        days=[]
        for i in range(0,len(raw_data)):
            try:
                temps.append(int(temp[i]))
            except:
                temps.append(np.nan)

        #dt=datetime.datetime(raw_data['Day'],raw_data['Time'])
        data ={'Date-Time':days,'Temp':temp}
        data2 = sm.datasets.sunspots.load_pandas().data['SUNACTIVITY']


        print("Read File: ",filepath.get())
        return
    def Experiment_AR():

        ar = AutoReg(temps,10).fit()
        output=ar.predict(0,len(ar.data.orig_endog))

        # The following is purely output, data cleaning has already accured by this point
        file=open("AR_OUTPUT.csv",'w')
        for i in range(0,len(ar.data.orig_endog)-1):
            print(ar.data.orig_endog[i]," ",output[i])
            file.write(str(ar.data.orig_endog[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        file.close()
        return
    def Experiment_ARX():
        arx = AutoReg(temps,10, exog=humids).fit()
        output = arx.predict(0, len(arx.data.orig_endog)-1)

        #The following is purely output, data cleaning has already accured by this point
        file=open("ARX_OUTPUT.csv",'w')
        for i in range(0,len(arx.data.orig_endog)-1):
            print(arx.data.orig_endog[i], " ", output[i])
            file.write(str(arx.data.orig_endog[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        file.close()
        return
    def Experiment_KNN():
        knn=KNeighborsRegressor()
        #alt_temps=temps.reshape(-1,1)
        #temps.reshape(-1,1)
        indexes=[]
        knn_temps=[]
        for i in range(0, len(temps)):
            indexes.append([i])
            #knn_temps.append([temps[i]])
        #knn.fit(knn_temps, indexes)
        knn.fit(indexes,temps)
        output=knn.predict(indexes)

        file=open("KNN_OUTPUT.csv",'w')
        for i in range(0,len(output)):
            file.write(str(temps[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        #mse = sk.mean_squared_error()
        file.close()
        return
    def Experiment_SWP(): #consider change

        k=14 #temp?
        arr=[]
        arr=temps.copy()
        from scipy.spatial import distance
        for i in range(2*k+1, len(arr)):

            sig_w=0.0
            sig_w_x=0.0
            window=[]
            for j in range(i-(2*k),i): #i or 0?
                #w=1/abs(arr[i]-arr[i-j])
                w=1/distance.euclidean((i,arr[i]),(i-j,arr[i-j]))
                #w=1/(math.dist((i,arr[i]),(i-j,arr[i-j])))
                sig_w=sig_w+w
                sig_w_x=sig_w_x+(w*arr[i-j])
                window.append(arr[i-j])
            #print(i)
            st_dev=statistics.stdev(window)
            x=sig_w_x/sig_w
            print(x,"=",sig_w_x,"/",sig_w)
            #t=#t-distribution

            PCI=x+(t.ppf(q=0.01,df=2*k-1)*st_dev*math.sqrt(abs(1-(1/2*k))))
            #print(PCI)
            #PCI=temp[i+1]+(perc*st_dev*math.sqrt(1-(1/2*k)))
            if(abs(arr[i])<abs(PCI)):
                arr[i]=x

        file=open("SWP_OUPUT.csv", 'w')
        for i in range(0,len(arr)):
            file.write(str(temps[i]))
            file.write(",")
            file.write(str(arr[i]))
            file.write("\n")
        return
    def Experiment_KNNI():
        knni = KNNImputer()

        indexes = []
        knn_temps = []
        for i in range(0, len(temps)):
            indexes.append([i])
            knn_temps.append([temps[i]])
        # knn.fit(knn_temps, indexes)
        knni.fit(indexes, temps)

        output = knni.predict(indexes)


        return
    def Experiment_WKNNI():
        return
    def Experiment_Expect_Max(): #Defunct
        array=[]
        MVs=[]
        for i in range(0, len(temps)):
            if(temps[i]>=0 or temps[i]<=0):
                array.append([temps[i], i])
            else:
                MVs.append(i)

        array=np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
        EM=GaussianMixture(n_components=2, random_state=0).fit(array, y=None)
        EM.means_
        return

    def func():  # function of the button
        tkinter.messagebox.showinfo("Greetings", "Hello! Welcome to PythonGeeks.")

    btn = Button(win, text="Autoregression", width=20, height=3, command=Experiment_AR)
    btn.place(x=200, y=20)
    btn = Button(win, text="Autoregression\n(exogenous inputs)", width=20, height=3, command=Experiment_ARX)
    btn.place(x=200, y=80)
    btn = Button(win, text="KNN",width=20, height=3, command=Experiment_KNN)
    btn.place(x=200, y=140)
    btn = Button(win, text="Sliding Window\nProjection", width=20, height=3, command=Experiment_SWP)
    btn.place(x=200, y=200)
    btn = Button(win, text="KNNI", width=20, height=3, command=Experiment_KNNI)
    btn.place(x=200, y=260)
    btn = Button(win, text="WKNNI", width=20, height=3, command=Experiment_WKNNI)
    btn.place(x=200, y=320)
    btn = Button(win, text="Maximum Likelihood\nImputiation", width=20, height=3, command=Experiment_Expect_Max)
    btn.place(x=200, y=380)

    filepath = Entry()
    filepath.pack
    filepath.focus_set()
    filepath.place(x=0, y=200)

    btn = Button(win, text="Read File", width=20, height=3, command=Read_File)
    btn.place(x=0, y=20)
    btn = Button(win, text="Read File\n(With MVs)", width=20, height=3, command=Read_File_MV)
    btn.place(x=0, y=80)

    win.mainloop()  # running the loop that works as a trigger



if __name__ == '__main__':
    start_gui()

