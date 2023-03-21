for i in range(1,13):
    if(i<10):
        filepath="C:\\Users\\sam\\Downloads\\Caltrans Data\\d04_text_station_hour_2022_0"
    else:
        filepath = "C:\\Users\\sam\\Downloads\\Caltrans Data\\d04_text_station_hour_2022_"
    filepath=filepath+str(i) +".txt"
    print(filepath)
    #filepath=input("Filepath")
    #keep=int(input("What do you want to keep"))
    keep=424031
    file=open(filepath)
    #df=file.read()
    lines=file.readlines()
    new=[]
    for i in range(0,len(lines)):
        elements=lines[i].split(',')
        if(int(elements[1])==keep):
            new.append(lines[i])
    #print(new)
    file.close()
    file=open(filepath+".csv",'w')
    file.writelines(new)
    file.close()