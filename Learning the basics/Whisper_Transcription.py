import whisper, os, tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

##################################################################
#Window Initalistion
#################################################################

#Creating the window and setting the properties
window = tk.Tk() 
window_width = 650
window_height = 325
window_size = str(window_width)+'x'+str(window_height)
window.geometry(window_size)

#Adding the window title and icon
window.title("OpenAI Whisper Transcription (Base)")
ico = Image.open('Images/TheWhiteDot_Logo.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

####################################################################
#Varibles
####################################################################

filename = ""
Transcription = ""

####################################################################
#Functions
####################################################################

def open():
    input_path = askopenfilename()
    print(input_path)
    global filename
    filename = input_path
    global setfilename
    setfilename = True

    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)

    T.delete("1.0", tk.END)

    print("DEBUG - Browse file button presssed")

    return input_path, filename, setfilename
    
def transcribe():
    
    print("DEBUG - Transcription initialisation")
    print("filename is " + filename)
    
    #Loads the Whisper model to use for transcription
    model = whisper.load_model('base')

    #Setting what should be transcribed
    result = model.transcribe(filename, fp16 = False, language="en")

    print("DEBUG - Transcription Complete")
    global Transcription
    Transcription = (result['text'])
    
    T.delete("1.0", tk.END)
    T.insert(tk.END, Transcription.strip())

    #TranscriptionTextFile()

    return result, Transcription

def TranscriptionTextFile():
    
    #Create a blank text file
    f = open("Test2.txt", "w")

    #Writing the transscribed text
    f.write(Transcription['text'])

    #Opens the transcription in notepad
    os.startfile('Test2.txt')

####################################################################
#Drawing the interface button and text etc.
####################################################################

#Creating the Main Label
l = tk.Label(window, text = "OpenAI Whisper Transcription (Base)")
l.config(font = ("Calibri, 12"))
l.grid(column=0, row=0, sticky = tk.NW, columnspan=2, padx=(10,10), pady=(10,10))

#Creating the open file button in the window
OpenFileButton = tk.Button(window, text="Browse File",width = 10, command=open)
OpenFileButton.grid(column=0, row=1, sticky = tk.NW, padx=(10,10), pady=(10,10))
OpenFileButton.config(font = ("Calibri, 8"))

#Drawing the file path
input_entry = tk.Entry(window, text="", width=85)
input_entry.grid(column=1, row=1, sticky = tk.W, padx=(10,10), pady=(10,10))
input_entry.config(font = ("Calibri, 8"))

#Creating the transcribe button in the window
TranscribeButton = tk.Button(window, text="Transcribe", width = 10, command=transcribe)
TranscribeButton.grid(column=0, row = 2, sticky = tk.NW, padx=(10,10), pady=(10,10))
TranscribeButton.config(font = ("Calibri, 8"))

T = tk.Text(window, height = 13, width = 85)
T.grid(column=1 , row = 2, sticky = tk.NW, padx=(10,10), pady=(10,10))
T.config(font = ("Calibri, 8"))

#####################################################################
#tkinter main loop
#####################################################################

window.mainloop()