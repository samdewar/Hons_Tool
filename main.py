import csv
import math
import statistics
import tkinter.messagebox
from tkinter import *
from timeit import default_timer
#import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
import sklearn as sk
from sklearn.neighbors import KNeighborsRegressor, NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
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
        global endog_var
        global exog_var
        exog_var=[]
        endog_var=[]
        raw_data = pd.read_csv("OT4.csv")

        temp=raw_data['Column 3']
        humid=raw_data['Column 4']

        days=[]
        for i in range(0,len(raw_data)):
            endog_var.append(int(temp[i]))
            exog_var.append(int(humid[i]))

        #dt=datetime.datetime(raw_data['Day'],raw_data['Time'])
        data ={'Date-Time':days,'Temp':temp}
        data2 = sm.datasets.sunspots.load_pandas().data['SUNACTIVITY']


        print("Read File: ",filepath.get())
        return

    def Read_File_MV():
        global raw_data
        global data
        global endog_var
        endog_var=[]
        raw_data = pd.read_csv("CALTRANS\\MV1.csv")

        temp=raw_data['Column 11']
        days=[]
        for i in range(0,len(raw_data)):
            try:
                endog_var.append(int(temp[i]))
            except:
                endog_var.append(np.nan)

        #dt=datetime.datetime(raw_data['Day'],raw_data['Time'])
        data ={'Date-Time':days,'Temp':temp}
        data2 = sm.datasets.sunspots.load_pandas().data['SUNACTIVITY']


        print("Read File: ",filepath.get())
        return
    def Experiment_AR():


        start=default_timer()
        ar = AutoReg(endog_var, 10, missing='drop').fit()

        output=ar.predict(0,len(ar.data.orig_endog))
        print(default_timer()-start)

        # The following is purely output, data cleaning has already finished by this point
        file=open("AR_OUTPUT.csv",'w')
        for i in range(0,len(ar.data.orig_endog)-1):
            #print(ar.data.orig_endog[i]," ",output[i])
            file.write(str(ar.data.orig_endog[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        file.close()
        return
    def Experiment_ARX():
        start=default_timer()
        arx = AutoReg(endog_var, 10, exog=exog_var, missing='drop').fit()
        output = arx.predict(0, len(arx.data.orig_endog)-1)
        print(default_timer()-start)
        #The following is purely output, data cleaning has already accured by this point
        file=open("ARX_OUTPUT.csv",'w')
        for i in range(0,len(arx.data.orig_endog)-1):
            #print(arx.data.orig_endog[i], " ", output[i])
            file.write(str(arx.data.orig_endog[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        file.close()
        return

    def Experiment_AR_Imputation():
        arr = endog_var
        MVs = []
        for i in range(0, len(arr)):
            try:
                temp=0
                temp=int(arr[i])+1
            except:
                MVs.append(i)

        start = default_timer()
        imputes=[]
        for i in range(0, len(MVs)):
            #print(i)

            ar = AutoReg(arr[0:MVs[i]],1).fit()
            arr[MVs[i]] = ar.forecast()[0]

            #imputes.append(ar.forecast())

        print(default_timer()-start)
        file=open("AR_IMPUTE_OUTPUT.csv", 'w')
        for i in range(0, len(arr)):
            file.write(str(arr[i]))
            file.write('\n')
        file.close()
        return
    def Experiment_KNN():
        # knn=KNeighborsRegressor() #not doing knn regression
        # #alt_temps=temps.reshape(-1,1)
        # #temps.reshape(-1,1)
        # indexes=[]
        # knn_temps=[]
        # for i in range(0, len(endog_var)):
        #     indexes.append([i])
        #     #knn_temps.append([temps[i]])
        # #knn.fit(knn_temps, indexes)
        # knn.fit(indexes, endog_var)
        # output=knn.predict(indexes)

        indexes = []
        knn_var = []
        for i in range(0, len(endog_var)):
            indexes.append([i])
            knn_var.append([endog_var[i]])


        knn=KNeighborsClassifier()
        start = default_timer()
        knn.fit(indexes,knn_var)
        output=knn.predict(knn_var)
        print(default_timer()-start)


        file=open("KNN_OUTPUT.csv",'w')
        for i in range(0,len(output)):
            file.write(str(endog_var[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        #mse = sk.mean_squared_error()
        file.close()
        return
    def Experiment_WKNN():
        knn=KNeighborsRegressor(weights='distance')
        #alt_temps=temps.reshape(-1,1)
        #temps.reshape(-1,1)
        indexes=[]
        knn_temps=[]
        for i in range(0, len(endog_var)):
            indexes.append([i])
            #knn_temps.append([temps[i]])
        #knn.fit(knn_temps, indexes)
        start = default_timer
        knn.fit(indexes, endog_var)
        output=knn.predict(indexes)
        print(default_timer-start)
        file=open("WKNNI_OUTPUT.csv",'w')
        for i in range(0,len(output)):
            file.write(str(endog_var[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        #mse = sk.mean_squared_error()
        file.close()
        return

    def Experiment_SWP(): #consider change

        k=14 #temp?
        arr=[]
        arr=endog_var.copy()
        from scipy.spatial import distance
        start = default_timer()
        for i in range(2*k+1, len(arr)):

            sig_w=0.0
            sig_w_x=0.0
            window=[]
            for j in range(i-(2*k),i):
                w=1/distance.euclidean((i,arr[i]),(i-j,arr[i-j]))
                sig_w=sig_w+w
                sig_w_x=sig_w_x+(w*arr[i-j])
                window.append(arr[i-j])
            x=sig_w_x/sig_w

            st_dev=statistics.stdev(window)

            PCI=x+(t.ppf(q=0.01,df=2*k-1)*st_dev*math.sqrt(abs(1-(1/2*k))))
            if(abs(arr[i])<abs(PCI)):
                arr[i]=x
        end=default_timer()-start
        print(end)
        file=open("SWP_OUPUT.csv", 'w')
        for i in range(0,len(arr)):
            file.write(str(endog_var[i]))
            file.write(",")
            file.write(str(arr[i]))
            file.write("\n")
        file.close()
        return


    def Experiment_KNNI():
        knni = KNNImputer(weights='uniform')
        indexes = []
        knn_var = []
        for i in range(0, len(endog_var)):
            indexes.append([i])
            knn_var.append([endog_var[i]])
        # knn.fit(knn_temps, indexes)
        start = default_timer()
        knni.fit(indexes, endog_var)
        output = knni.fit_transform(knn_var)
        print(default_timer()-start)
        file = open("KNNI_OUTPUT.csv",'w')
        for i in range(0,len(output)):
            #file.write(str(endog_var[i]))
            #file.write(",")
            file.write(str(output[i][0]))
            file.write("\n")
        file.close()
        return
    def Experiment_WKNNI():
        wknni = KNNImputer(weights='distance')

        indexes = []
        knn_temps = []
        for i in range(0, len(endog_var)):
            indexes.append([i])
            knn_temps.append([endog_var[i]])

        start = default_timer()
        wknni.fit(indexes, endog_var)
        output = wknni.fit_transform(knn_temps)
        print(default_timer()-start)
        file=open("WKNNI_OUTPUT.csv", 'w')
        for i in range(0,len(output)):
            file.write(str(output[i][0]))
            file.write("\n")
        file.close()
        return
    def Experiment_Expect_Max(): #Defunct
        array=[]
        MVs=[]
        for i in range(0, len(endog_var)):
            if(endog_var[i]>=0 or endog_var[i]<=0):
                array.append([endog_var[i], i])
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
    btn = Button(win, text="Autoregression Based\nImputiation", width=20, height=3, command=Experiment_AR_Imputation)
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

