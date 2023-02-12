import csv
import tkinter.messagebox
from tkinter import *
#import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import KNNImputer
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
        temps=[]
        raw_data = pd.read_csv("output.csv")

        temp=raw_data['Temp']


        days=[]
        for i in range(0,len(raw_data)):
            #day=raw_data.at[i,'Day'].split("/")
            #t=raw_data.at[i,'Time'].split(":")
            temps.append(int(temp[i]))
            #days.append(datetime.datetime(int(day[2]),int(day[1]),int(day[0]),int(t[0]),int(t[1]))) #or something

            print(i)

        #dt=datetime.datetime(raw_data['Day'],raw_data['Time'])
        data ={'Date-Time':days,'Temp':temp}
        data2 = sm.datasets.sunspots.load_pandas().data['SUNACTIVITY']


        print("Read File: ",filepath.get())
        return
    def Experiment_AR():

        ar = AutoReg(temps,300).fit()

        print(ar.data.endog)
        print(ar.data.orig_endog)
        file=open("test_finished.csv",'a')

        for i in range(0,len(ar.data.orig_endog)):
            file.write(str(ar.data.orig_endog[i]))
            file.write(",")
            file.write(str(ar.data.endog[i]))
            file.write("\n")

        return
    def Experiment_ARX():
        return
    def Experiment_KNN():
        return
    def Experiment_SWP(): #consider change
        return
    def Experiment_KNNI():
        return
    def Experiment_WKNNI():
        return
    def Experiment_Expect_Max():
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

    win.mainloop()  # running the loop that works as a trigger



if __name__ == '__main__':
    start_gui()

