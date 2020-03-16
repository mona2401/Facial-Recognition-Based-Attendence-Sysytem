# Facial-Recognition-Based-Attendence-System
## SOFTWARE USED: - 
### 	Python 
### Tkinter GUI Interface 
### 	OpenCV (Version 4)

## How It Works: -
### Take Images: -

#### When we run train.py a window is opened and ask for Enter Id and Enter Name. After enter name and id then we have to click Take Images button. By clicking Take Images camera of running computer is opened and it start taking image sample of person. This Id and Name is stored in folder Student Details and file name Student Details.csv. It takes 30 images as sample and store them in folder Dataset. After completion it notify that Images saved for This Id and This Name with a Thank you.
### Train Images: -

#### click Train Image button. Now it takes few seconds to train machine for the images that are taken by clicking Take Image button and creates a Trainner.yml file and store in recognizer folder.
### Track Images: -

#### Now By clicking Track Image button camera of running machine is opened again. If face is recognised by system then Id and Name of person is shown on Image. Any other person rather than the person’s trained images will be An Unknown to the computer so it will display Unknown. Press Q for quit the window. After quitting it attendance of person will be stored in Attendance folder as csv file with name, id, date and time.
### GET AN EMAIL: -
#### This is a optional thing. This notifies the student that their attendance is successfully registered. This is done by SMTP Library the port number may different from computers to computers. And you have to allow the access of your google account otherwise this won’t work. 


## Made By
## Monalisa Panda
