import csv
import math
import statistics
import time
import tkinter.messagebox
from tkinter import *
from timeit import default_timer
#import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from numpy import zeros
from scipy.linalg import toeplitz
from statsmodels.tsa.ar_model import AutoReg
import sklearn as sk
from sklearn.neighbors import KNeighborsRegressor, NearestNeighbors
from sklearn.experimental import enable_iterative_imputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import KNNImputer, IterativeImputer
from sklearn.mixture import GaussianMixture
from scipy.stats import t
import datetime
#import autoregression

global filepath
#global raw_data
# global endog_var
# endog_var=[]

def start_gui():
    win = Tk()  # creating the main window and storing the window object in 'win'
    win.title('Welcome')  # setting title of the window
    win.geometry('500x500')  # setting the size of the window

    filepath = Entry()
    filepath.pack
    filepath.focus_set()
    filepath.place(x=0, y=200)


    def Read_File():
        global raw_data
        global data
        global endog_var
        global exog_var
        exog_var=[]
        endog_var=[]
        tkinter.messagebox.showinfo("Time", "Information")
        # raw_data = pd.read_csv("OT4.csv")
        raw_data = pd.read_csv(filepath.get())
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
        global exog_var
        global alt_data
        alt_data=[]
        exog_var=[]
        endog_var=[]
        # raw_data = pd.read_csv("CALTRANS\\MV4.csv")
        raw_data=pd.read_csv(filepath.get())
        temp=raw_data['Column 11']
        temp2=raw_data['Column 12']
        temp3=raw_data['Other Station']
        days=[]
        for i in range(0,len(raw_data)):
            exog_var.append(temp2[i])
            alt_data.append(temp3[i])
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
        tkinter.messagebox.showinfo("Time", default_timer()-start)

        # The following is purely output, data cleaning has already finished by this point
        file=open("AR_OUTPUT.csv",'w')
        for i in range(0,len(ar.data.orig_endog)-1):
            #tkinter.messagebox.showinfo("Time", ar.data.orig_endog[i]," ",output[i])
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
        tkinter.messagebox.showinfo("Time", default_timer()-start)
        #The following is purely output, data cleaning has already accured by this point
        file=open("ARX_OUTPUT.csv",'w')
        for i in range(0,len(arx.data.orig_endog)-1):
            #tkinter.messagebox.showinfo("Time", arx.data.orig_endog[i], " ", output[i])
            file.write(str(arx.data.orig_endog[i]))
            file.write(",")
            file.write(str(output[i]))
            file.write("\n")
        file.close()
        return

    def Experiment_AR_Based_Imputation():
            arr = endog_var.copy()
            MVs=[]
            for i in range(0, len(arr)):
                try:
                    temp = 0
                    temp = int(arr[i]) + 1
                except:
                    MVs.append(i)
                    arr[i]=0
            ar = AutoReg(arr, 10, missing='drop').fit()
            output =ar.predict(MVs[0])
            coef=ar.params
            T = toeplitz(coef)
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
            #tkinter.messagebox.showinfo("Time", i)

            ar = AutoReg(arr[0:MVs[i]],1).fit()

            arr[MVs[i]] = ar.forecast()[0]

            #imputes.append(ar.forecast())

        tkinter.messagebox.showinfo("Time", default_timer()-start)
        file=open("AR_IMPUTE_OUTPUT.csv", 'w')
        for i in range(0, len(arr)):
            file.write(str(arr[i]))
            file.write('\n')
        file.close()
        return

    def Experiment_IterativeImputer():
        imputer=IterativeImputer(initial_strategy="mean", max_iter=10, estimator=KNeighborsRegressor())

        indexes=[]
        arr=[]

        for i in range(0, len(endog_var)):
            temp=[]
            temp.append(endog_var[i])
            temp.append(i)
            arr.append(temp)

        start = default_timer()
        imputer.fit(arr)

        output=imputer.transform(arr)
        tkinter.messagebox.showinfo("Time", default_timer()-start)
        file=open("Iterative_Imputer_OUTPUT.csv",'w')
        for i in range (0,len(output)):
            file.write(str(output[i][0]))
            file.write('\n')
        file.close()
        return


    def Experiment_KNN():
        indexes = []
        knn_var = []
        for i in range(0, len(endog_var)):
            indexes.append([i])
            knn_var.append([[endog_var[i]],[i]])


        knn=KNeighborsClassifier()
        start = default_timer()
        knn.fit(indexes,knn_var)
        output=knn.predict(knn_var)
        tkinter.messagebox.showinfo("Time", default_timer()-start)


        file=open("KNN_OUTPUT.csv",'w')
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
        tkinter.messagebox.showinfo("Time", end)
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
        tkinter.messagebox.showinfo("Time", default_timer()-start)
        file = open("KNNI_OUTPUT.csv",'w')
        for i in range(0,len(output)):
            #file.write(str(endog_var[i]))
            #file.write(",")
            file.write(str(output[i][0]))
            file.write("\n")
        file.close()
        return
    # def Experiment_WKNNI():
    #     arr = endog_var
    #     MVs = []
    #     for i in range(0, len(arr)):
    #         try:
    #             temp = 0
    #             temp = int(arr[i]) + 1
    #         except:
    #             MVs.append(i)
    #
    #     start = default_timer()
    #     imputes = []
    #     for i in range(0, len(MVs)):
    #         # tkinter.messagebox.showinfo("Time", i)
    #
    #         ar = AutoReg(arr[0:MVs[i]], exog=exog_var[0:MVs[i]], lags=1).fit()
    #         arr[MVs[i]] = ar.forecast()[0]
    #
    #
    #         # imputes.append(ar.forecast())
    #
    #     tkinter.messagebox.showinfo("Time", default_timer() - start)
    #     file = open("ARX_IMPUTE_OUTPUT.csv", 'w')
    #     for i in range(0, len(arr)):
    #         file.write(str(arr[i]))
    #         file.write('\n')
    #     file.close()
    #     return




    def Experiment_SWPI(): #consider change
        k=5 #temp?
        arr=[]

        arr=endog_var.copy()
        from scipy.spatial import distance
        start = default_timer()
        for i in range(2*k+1, len(arr)):
            try:
                temp=int(arr[i])+1
            except:
                sig_w=0.0
                sig_w_x=0.0
                window=[]
                for j in range(i-(2*k),i):
                    #w=1/distance.euclidean((i,arr[i]),(i-j,arr[i-j]))
                    #w=1/((i-arr[i])^2+(i-j-arr[i-j]))^2
                    w=1/i-j
                    sig_w=sig_w+w
                    sig_w_x=sig_w_x+(w*arr[i-j])
                    window.append(arr[i-j])
                x=sig_w_x/sig_w
                #st_dev=statistics.stdev(window)
                #PCI=x+(t.ppf(q=0.01,df=2*k-1)*st_dev*math.sqrt(abs(1-(1/2*k))))
                arr[i]=x
        end=default_timer()-start
        tkinter.messagebox.showinfo("Time", end)
        file=open("SWPI_OUPUT.csv", 'w')
        for i in range(0,len(arr)):
            file.write(str(endog_var[i]))
            file.write(",")
            file.write(str(arr[i]))
            file.write("\n")
        file.close()
        return

    def Example_Algo():
        start=default_timer()
        time.sleep(100)
        tkinter.messagebox.showinfo("Time", start-default_timer())


    btn = Button(win, text="Read File", width=20, height=3, command=Read_File)
    btn.place(x=0, y=20)
    btn = Button(win, text="Read File\n(With MVs)", width=20, height=3, command=Read_File_MV)
    btn.place(x=0, y=80)

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
    btn = Button(win, text="SWP Based\nImputation", width=20, height=3, command=Experiment_SWPI)
    btn.place(x=200, y=320)
    btn = Button(win, text="Iterative Imputer", width=20, height=3, command=Experiment_IterativeImputer)
    btn.place(x=200, y=380)

    win.mainloop()  # running the loop that works as a trigger

if __name__ == '__main__':
    start_gui()

