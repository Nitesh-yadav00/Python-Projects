#This code creates a simple video editor GUI using Python's Tkinter library. 
#It allows users to perform three main video editing functions:
#  Concatenate Videos: Combines two video clips into one.
#  Mute Video: Removes the audio track from a video.
#  Trim Video: Cuts a segment from a video based on specified start and end times.

from moviepy.editor import *
import tkinter as tk
from tkinter import filedialog

def combine(clip1path,clip2path):
    clip1=VideoFileClip(clip1path)
    clip2=VideoFileClip(clip2path)
    combined=concatenate_videoclips([clip1,clip2])
    combined.write_videofile("/Users/capta/Desktop/0/combined1.mp4")

def combinebutton():
    clip1path=clippath1ref.get()
    clip2path=clip2pathref.get()

    try:
        combine(clip1path,clip2path)
    
    except:
        pass

def mute(clip1path):
    clip1=VideoFileClip(clip1path)
    muteclip=clip1.without_audio()
    muteclip.write_videofile("/Users/capta/Desktop/0/mute.mp4")

def mutebutton():
    clip1path=clippath1ref.get()
    try:
        mute(clip1path)
    except:
        pass

def trim(clip1path,From,To):
    clip1=VideoFileClip(clip1path).cutout(From,To)
    clip1.write_videofile("/Users/capta/Desktop/0/trimmedclip.mp4")


def trimbutton():
    clip1path=clippath1ref.get()
    trimfrom=Fromref.get()
    trimto=Toref.get()
    try:
        trim(clip1path,trimfrom,trimto)
    except:
        pass

root=tk.Tk()
root.title("Video Editor")

tk.Label(root,text="clip1").grid(row=0,column=0,padx=10,pady=10)
clippath1ref=tk.Entry(root,width=50)
clippath1ref.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root,text="Browse",command=lambda:clippath1ref.insert(0,filedialog.askdirectory())).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root,text="clip2").grid(row=1,column=0,padx=10,pady=10)
clip2pathref=tk.Entry(root,width=50)
clip2pathref.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root,text="browse",command=lambda:clip2pathref.insert(0,filedialog.askdirectory())).grid(row=1, column=2, padx=10, pady=10)

Concatenate= tk.Button(root, text="Concatenate", command=combinebutton)
Concatenate.grid(row=2, column=0, columnspan=3, pady=20)

Mutebutton= tk.Button(root, text="Mute", command=mutebutton)
Mutebutton.grid(row=3, column=0, columnspan=3, pady=20)

tk.Label(root, text=" from (HH:MM:SS):").grid(row=4, column=0, padx=10, pady=10)
Fromref= tk.Entry(root)
Fromref.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text=" to (HH:MM:SS):").grid(row=5, column=0, padx=10, pady=10)
Toref= tk.Entry(root)
Toref.grid(row=5, column=1, padx=10, pady=10)

Trimbutton= tk.Button(root, text="Trim", command=trimbutton)
Trimbutton.grid(row=6, column=0, columnspan=3, pady=20)


root.mainloop()
