import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from pytube import YouTube
import subprocess

# Function to open file dialog for selecting the directory
def select_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, selected_directory)

# Function to download the YouTube video
def download_video():
    url = url_entry.get()
    directory = directory_entry.get()
    video = YouTube(url)
    #myvideo = video.streams.get_highest_resolution()
    streams = video.streams.filter(res="1080p")
    selected_stream = streams.first()
    if selected_stream != None:
        myvideo = video.streams.filter(res="1080p")
        audio = video.streams.get_audio_only()
        #downloading and renaming the audio
        name = audio.default_filename
        temp = "temp.mp3"
        audio.download(output_path = directory)
        ffmpegcommand = ["ffmpeg","-y","-i", directory + '\\' + name , directory + '\\' + temp]
        subprocess.run(ffmpegcommand)
        selected_stream = myvideo.first()
        selected_stream.download(output_path = directory)
        input_video = directory + '\\' + name
        output_video = directory + '\\' + "temp2.mp4"
        input_audio = directory + '\\' + temp
        ffmpeg_command = [
            'ffmpeg',
            '-y',  # Add the -y flag here to force overwrite
            '-i', input_video,
            '-i', input_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            output_video
        ]
        subprocess.run(ffmpeg_command)

        #cleaning up all the temp files
        os.remove(input_audio)
        os.remove(input_video)

        #renaming our output file to original video name
        os.rename(output_video, input_video)


    else:
        myvideo = video.streams.get_highest_resolution()
        myvideo.download(output_path = directory)
   
    
    

    #myvideo2 = video.streams.get_highest_resolution()
    #myvideo.download(output_path = directory)
    
    # Add your download logic here
    
    # For now, let's print the URL and directory
    # print("URL:", url)
    # print("Directory:", directory)


def on_entry_click(event):
    if entry_var.get() == "URL":
        entry_var.set("")  # Clear the placeholder text when clicked

def on_entry_leave(event):
    if entry_var.get() == "":
        entry_var.set("Enter text here")

# Create the main window
root = tk.Tk()
root.geometry("1280x720")
root.title("YouTube Video Downloader")
root.configure(bg="white")
# Create a red rectangle with a black shadow
rectangle = tk.Canvas(root, width=500, height=2000, bg="red", highlightbackground="black", highlightthickness=15)
rectangle.place(relx=0, rely=0, anchor="center")

# Label for "YouTube Video Downloader"
title_label = tk.Label(root, text="YouTube Video Downloader", font=("Helvetica", 20, "bold"))
title_label.configure(bg="white")
title_label.place(relx=0.57, rely=0.3, anchor="center")

#Input box style - doesn't work
style = ttk.Style()
style.configure("Rounded.TEntry", borderwidth=2, relief="solid")

# Input box for URL
# url_label = tk.Label(root, text="URL:")
# url_label.place(relx=0.35, rely=0.4, anchor="e")
entry_var = tk.StringVar()
entry_var.set("URL")
url_entry = ttk.Entry(root, width=50,textvariable=entry_var,style="Rounded.TEntry")
url_entry.bind("<FocusIn>", on_entry_click)  # Bind the click event to clear the placeholder
url_entry.bind("<FocusOut>", on_entry_leave) 
#url_entry.pack() 
url_entry.place(relx=0.45, rely=0.4, anchor="w")

# Input box for directory
entry_var2 = tk.StringVar()
entry_var2.set("E:\current file edits new")
# directory_label = tk.Label(root, text="Save to:")
# directory_label.place(relx=0.35, rely=0.5, anchor="e")
directory_entry = ttk.Entry(root, width=50,textvariable = entry_var2,style="Rounded.TEntry")
directory_entry.place(relx=0.45, rely=0.5, anchor="w")

# Browse button
browse_button = ttk.Button(root, text="Browse", command=select_directory)
browse_button.place(relx=0.70, rely=0.5, anchor="w")

# Go button
go_button = tk.Button(root,width=10, text="Go", bg = "green",fg = "white", command=download_video)
go_button.place(relx=0.555, rely=0.6, anchor="center")

# Configure a green style for the Go button
style = ttk.Style()
style.configure("Green.TButton", color="green", foreground="white")

root.mainloop()
