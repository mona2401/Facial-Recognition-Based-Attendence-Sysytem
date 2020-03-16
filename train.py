import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from playsound import playsound
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import smtplib
import random as r
import matplotlib.pyplot as plt


window = tk.Tk()
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
window.configure(background='white')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="Face-Recognition-Based-Attendance-System" ,bg="blue"  ,fg="white"  ,width=50  ,height=3,font=('sans-serif', 25, 'italic bold underline')) 
message.place(x=150, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="black" ,font=('sans-serif', 15, ' bold ') ) 
lbl.place(x=250, y=160)

txt = tk.Entry(window,width=20  ,bg="#A9FF33" ,fg="black",font=('sans-serif', 15, ' bold '))
txt.place(x=550, y=175)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="black"    ,height=2 ,font=('sans-serif', 15, ' bold ')) 
lbl2.place(x=250, y=240)

txt2 = tk.Entry(window,width=20  ,bg="#A9FF33"  ,fg="black",font=('sans-serif', 15, ' bold ')  )
txt2.place(x=550, y=255)

lbl4 = tk.Label(window, text="Email : ",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('sans-serif', 15, 'bold')) 
lbl4.place(x=250, y=320)

email = tk.Entry(window,width=20  ,bg="#A9FF33"  ,fg="black",font=('sans-serif', 15, ' bold ')  )
email.place(x=550, y=335)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('sans-serif', 15, ' bold underline ')) 
lbl3.place(x=250, y=400)

message = tk.Label(window, text="" ,bg="#A9FF33"  ,fg="black"  ,width=30  ,height=2, activebackground = "green" ,font=('sans-serif', 15, ' bold ')) 
message.place(x=550, y=415)

def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                sampleNum=sampleNum+1
                cv2.imwrite("Dataset\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('KUNU',img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum>=30:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    playsound('sound.mp3')
    

    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    detector =cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces,Id = getImagesAndLabels("Dataset")
    recognizer.train(faces, np.array(Id))
    recognizer.save("recognizer\Trainner.yml")
    res = "Images are Trained"
    message.configure(text= res)

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 100):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 150):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message.configure(text= res)

email=(email.get())
def GetanEmail():
    fromaddr="Your Email"
    toaddr=email
    msg=""
    for i in range(4):
        msg+=str(r.randint(1,9))
    username="Your Email"
    password="Your Password"
    server=smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr,toaddr,msg)
    print("Your Attendence is successful")
    server.quit();
    res="Mail send success"
    message.configure(text= res)



  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="white"  ,bg="green"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
clearButton.place(x=850, y=160)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="green"  ,width=20  ,height=2, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
clearButton2.place(x=850, y=260)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#FF4933"  ,width=15  ,height=3, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
takeImg.place(x=150, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="#FF4933"  ,width=15  ,height=3, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
trainImg.place(x=370, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="white"  ,bg="#FF4933"  ,width=15  ,height=3, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
trackImg.place(x=590, y=500)
email = tk.Button(window, text="Get an email", command=GetanEmail  ,fg="white"  ,bg="#FF4933"  ,width=15  ,height=3, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
email.place(x=810, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="#FF4933"  ,width=15  ,height=3, activebackground = "Red" ,font=('sans-serif', 15, ' bold '))
quitWindow.place(x=1030, y=500)
msg = tk.Label(window, text="Developed By Monalisa Panda" ,bg="white"  ,fg="Blue"  ,width=50  ,height=1,font=('sans-serif', 25, 'italic bold underline')) 
msg.place(x=150, y=600)
 
window.mainloop()
 
