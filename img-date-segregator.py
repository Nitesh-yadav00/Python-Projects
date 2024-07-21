#This code provides a graphical user interface (GUI) for segregating images based on their capture date and time. 
#Users can specify a source folder, a destination folder, a target date, and a time range. 
#The program will then copy images taken within the specified date and time range from the source folder to the destination folder. 
#It uses Python's Tkinter for the GUI, PIL for reading image metadata, and shutil for copying files. 
#The interface allows users to browse for folders and input the desired date and time range, 
#And displays a success or error message after attempting to segregate the images.
import os 
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime,time
import tkinter as tk
from tkinter import filedialog, messagebox

#function to find date and time 
def getimagetime(imagepath):
    try:
        image=Image.open(imagepath)
        #image._getexif() is a method call that retrieves the EXIF metadata from an image.
        #By calling image._getexif(), you can retrieve the EXIF metadata from the image as a dictionary-like object. 
        #Each key in the dictionary represents a tag,and the corresponding value represents the value of that tag
        metadata=image._getexif()
        if metadata:
            #The items() method is used to iterate over the key-value pairs 
            #in the metadata dictionary.
            for tag,value in metadata.items():
                taganme=TAGS.get(tag)
                if taganme == "DateTimeOriginal":
                   #The strptime function is used to parse a string representation of a date
                   #and time into a datetime object. It stands for "string parse time".
                   return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print("Error reading EXIF data")
    return None

#function to segregate images
def segregateimages(fromfolder,tofolder,starttimestr,endtimestr,desdatestr):
    #.time(): This line is calling the time() method on the datetime object returned by strptime. 
    #The time() method returns a time object representing the time component of the datetime object.
    starttime = datetime.strptime(starttimestr, '%H:%M').time()
    endtime = datetime.strptime(endtimestr, '%H:%M').time()
    desdate=datetime.strptime(desdatestr,'%d-%m-%Y').date()
    #this line of code is used to iterate over all the directories and files in the src_folder directory tree.
    #It provides the current directory (root), a list of directories within the current directory (dirs), and a list of files within the current directory (files). 
    #This allows you to perform operations on each directory and file within the specified directory tree.
    for root,dirs,files in os.walk(fromfolder):
        for file in files:
            if file.lower().endswith(('jpg','jpeg','png')):
               #this is a function provided by the os module in Python 
               #that joins one or more path components into a single path.
               imagepath=os.path.join(root,file)
               imagedatetime=getimagetime(imagepath)
               if imagedatetime:
                   imagedate=imagedatetime.date()
                   if imagedate==desdate:
                       if imagedatetime:
                        imagetime=imagedatetime.time()
                        if starttime<=imagetime<=endtime:
                            newpath = os.path.join(tofolder, file)
                            #shutil.move(): This is a function provided by the shutil module in Python. 
                            #It is used to move or rename a file or directory. 
                            #In this case, it is used to move a file from the imagepath to a new location specified by newpath
                            shutil.copy(imagepath,newpath)
            else:
                print("Files are not in jpg,png,jpeg format")


#button click 
def startbuttonclick():
    #.get(): This is a method that is commonly used with user interface elements to retrieve 
    #the value entered by the user.It retrieves the text or content entered in the user interface element.
    fromfolder = fromfolderref.get()
    tofolder= tofolderref.get()
    starttime=starttimeref.get()
    endtime=endtimeref.get()
    desdate=desdateref.get()
    try:
        segregateimages(fromfolder,tofolder,starttime,endtime,desdate)
        #messagebox is a module that provides functions for creating and displaying dialog boxes 
        #or message boxes in a graphical user interface (GUI) application.
        messagebox.showinfo("Success", "Images segregated successfully!")
    except Exception as e:
        messagebox.showerror("Error")

#GUI
root=tk.Tk()
root.title("Image Segregation Tool")

#fromfolder
#tk.Label: This is a class provided by the tkinter module in Python. It is used to create a label widget
tk.Label(root,text="from Folder").grid(row=0,column=0,padx=10,pady=10)
fromfolderref=tk.Entry(root,width=50)
fromfolderref.grid(row=0, column=1, padx=10, pady=10)
#tk.button parameters master(root),cnf(text,colour,command),**kw(extra arguments)
#lambda: The lambda keyword is used to create an anonymous function. It allows you to define a function without a name
#command=lambda: src_folder_entry.insert(0, filedialog.askdirectory()): This is an argument passed to the Button class. 
#It specifies the command or function that will be executed when the button is clicked
# insert() method of the src_folder_entry entry widget to insert the selected directory path at the beginning (index 0). 
#It uses the filedialog.askdirectory() function to open a directory selection dialog and retrieve the selected directory path.
tk.Button(root,text="Browse",command=lambda:fromfolderref.insert(0,filedialog.askdirectory())).grid(row=0, column=2, padx=10, pady=10)

#tofolder 
tk.Label(root,text="To Folder").grid(row=1,column=0,padx=10,pady=10)
tofolderref=tk.Entry(root,width=50)
tofolderref.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root,text="browse",command=lambda:tofolderref.insert(0,filedialog.askdirectory())).grid(row=1, column=2, padx=10, pady=10)

#date
tk.Label(root,text="date(DD-MM-YY)").grid(row=2,column=0,padx=10,pady=10)
desdateref=tk.Entry(root)
desdateref.grid(row=2,column=1, padx=10, pady=10)

#starttime
tk.Label(root, text="Start Time (HH:MM:SS):").grid(row=3, column=0, padx=10, pady=10)
starttimeref= tk.Entry(root)
starttimeref.grid(row=3, column=1, padx=10, pady=10)

#endtime
tk.Label(root, text="End Time (HH:MM:SS):").grid(row=4, column=0, padx=10, pady=10)
endtimeref= tk.Entry(root)
endtimeref.grid(row=4, column=1, padx=10, pady=10)

#start button 
startbutton= tk.Button(root, text="Start", command=startbuttonclick)
startbutton.grid(row=5, column=0, columnspan=3, pady=20)
root.mainloop()