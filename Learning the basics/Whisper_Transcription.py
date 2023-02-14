import whisper, os, tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

####################################################################
#Varibles
####################################################################

filename = ""
Transcription = ""
AppName = "OWATA"
AppDescription = "OpenAI Whisper Transcription App"

PrimaryColour = "#7fe0ec"
SecondaryColour ="#eeeeee"

##################################################################
#Window Initalistion
#################################################################

#Creating the window and setting the properties
window = tk.Tk() 
window_width = 700
window_height = 400
window_size = str(window_width)+'x'+str(window_height)
window.geometry(window_size)
#window.resizable(width=False, height=False)

#Adding the window title and icon
window.title(AppName)
ico = Image.open('Images/OWATA_LOGO.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)
#window.iconbitmap("Images/OWATA_LOGO.ico")

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

#Creating the blue background at the top
BlueBackground = tk.Frame(window, bg=PrimaryColour, width=window_width, height=60)
BlueBackground.grid(column=0, row=0, sticky = tk.NW, columnspan=1, padx=(0,0), pady=(0,1))
BlueBackground.grid_propagate(0)

WhiteBackground = tk.Frame(window, bg=SecondaryColour, width=window_width, height=(window_height - 75))
WhiteBackground.grid(column=0, row=2, sticky = tk.NW, columnspan=1, padx=(0,0), pady=(0,1))
WhiteBackground.grid_propagate(0)

#Creating the Main Label
l = tk.Label(BlueBackground, text = AppName)
l.config(font ="Calibri 32 bold", bg=PrimaryColour, fg=SecondaryColour)
#l.pack(side= tk.RIGHT)
l.grid(column=0, row=0, sticky = tk.NE, columnspan=1, padx=(10,10), pady=(1,1))

#Creating the Description
#l2 = tk.Label(BlueBackground, text = AppDescription)
#l2.config(font = "Calibri 12", bg="#7fe0ec", fg="white")
#l2.pack()
#l2.grid(column=0, row=1, sticky = tk.NW, columnspan=2, padx=(10,10), pady=(1,20))

#Creating the open file button in the window
OpenFileButton = tk.Button(WhiteBackground, 
                            text="Browse",
                            width = 10, height = 1,
                            bg=PrimaryColour,
                            relief = "flat",
                            command=open)
OpenFileButton.grid(column=0, row=2, sticky = tk.NW, padx=(20,10), pady=(20,10))
OpenFileButton.config(font = "Calibri 12", fg="white")

#Drawing the file path
input_entry = tk.Entry(WhiteBackground, text="", width=80)
input_entry.grid(column=1, row=2, sticky = tk.W, padx=(10,10), pady=(20,10))
input_entry.config(font = ("Calibri, 10"))

#Creating the transcribe button in the window
TranscribeButton = tk.Button(WhiteBackground,
                             text="Transcribe",
                             width = 10,
                             bg=PrimaryColour,
                             relief = "flat",
                             command=transcribe)
TranscribeButton.grid(column=0, row = 3, sticky = tk.NW, padx=(20,10), pady=(20,10))
TranscribeButton.config(font = "Calibri 12", fg="white")

T = tk.Text(WhiteBackground, height = 13, width = 80)
T.grid(column=1 , row = 3, sticky = tk.NW, padx=(10,10), pady=(10,10))
T.config(font = ("Calibri, 10"))

#####################################################################
#tkinter main loop
#####################################################################

window.mainloop()