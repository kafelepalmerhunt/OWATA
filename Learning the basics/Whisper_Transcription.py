import whisper, os, tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

####################################################################
#Varibles
####################################################################

filename = ""
Transcription = ""
AppName = "OWATA.ai"
#AppDescription = "OpenAI Whisper Transcription App"

PrimaryColour = "#73c9d3"
SecondaryColour = "#dddddd"

##################################################################
#Window Initalistion
#################################################################

#Creating the window and setting the properties
window = tk.Tk() 
window_width = 725
window_height = 380
window_size = str(window_width) + 'x' + str(window_height)
window.geometry(window_size)
window.resizable(width = False, height = False)

#Adding the window title and icon
window.title(AppName)
ico = Image.open('Images/OWATA_LOGO.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

####################################################################
#Functions
####################################################################

def openfile():
    
    #Opens the OS browse file window to select a file and path
    input_path = askopenfilename()

    #Making the variable global to be accesses/changed in other places
    global filename
    filename = input_path

    #Makes the var global to be accessed/changes in other places
    global setfilename
    setfilename = True
    
    #Deleted exisiting path (if exists) and adds the new one
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)

    #Deletes any text in the transcription box when choosing a new path
    T.delete("1.0", tk.END)

    return input_path, filename, setfilename
    
def transcribe():
       
    #Loads the Whisper model to use for transcription
    model = whisper.load_model('base')

    #Setting what should be transcribed
    result = model.transcribe(filename, fp16 = False, language="en")

    #Making the var global to be accessed/changed in other places
    global Transcription

    #Setting the var transcription as the result of the model.transcribe method
    Transcription = (result['text'])
    
    #Deletes any existing text in the transcription box
    T.delete("1.0", tk.END)

    #Adds the new transcription to the box and removes the space at the front via strip
    T.insert(tk.END, Transcription.strip())

    return result, Transcription

def TranscriptionTextFile():
    
    #Create a blank text file
    f = open("Test2.txt", "w")

    #Writing the transscribed text
    f.write(Transcription.strip())

    #Opens the transcription in notepad
    os.startfile('Test2.txt')

####################################################################
#Drawing the interface button and text etc.
####################################################################

#Creating the blue background at the top
BlueBackground = tk.Frame(window,
                            bg = PrimaryColour,
                            width = window_width,
                            height = 60)
BlueBackground.grid(column = 0, row = 0, sticky = tk.NW, columnspan = 1, padx = (0,0), pady = (0,1))
BlueBackground.grid_propagate(0)

#Creating the gey background for the main body
WhiteBackground = tk.Frame(window,
                            bg = SecondaryColour,
                            width = window_width,
                            height = (window_height))
WhiteBackground.grid(column = 0, row = 2, sticky = tk.NW, columnspan = 1, padx = (0,0), pady = (0,1))
WhiteBackground.grid_propagate(0)

#Creating the Main Label
l = tk.Label(BlueBackground,
             text = AppName)
l.config(font ="Calibri 32 bold", bg = PrimaryColour, fg = "white")
l.grid(column = 0, row = 0, sticky = tk.NE, columnspan = 1, padx = (10,10), pady = (1,1))

#Creating the open file button in the window
OpenFileButton = tk.Button(WhiteBackground, 
                            text = "Browse",
                            width = 10,
                            bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                            relief = "flat",
                            command = openfile)
OpenFileButton.grid(column = 0, row = 2, sticky = tk.NW, padx = (20,10), pady = (20,10))
OpenFileButton.config(font = "Calibri 12", fg = "white")

#Drawing the file path
input_entry = tk.Entry(WhiteBackground,
                        text = "", 
                        width = 80)
input_entry.grid(column = 1, row = 2, sticky = tk.W, padx = (10,10), pady = (20,10))
input_entry.config(font = ("Calibri, 10"))

#Creating the transcribe button in the window
TranscribeButton = tk.Button(WhiteBackground,
                             text  ="Transcribe",
                             width = 10,
                             bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                             relief = "flat",
                             command = transcribe)
TranscribeButton.grid(column = 0, row = 3, sticky = tk.NW, padx = (20,10), pady = (20,10))
TranscribeButton.config(font = "Calibri 12", fg = "white")

#Creating the transcription text window
T = tk.Text(WhiteBackground,
            height = 13, 
            width = 80, 
            relief = "groove")
T.grid(column = 1 , row = 3, sticky = tk.NW, padx = (10,10), pady = (10,10))
T.config(font = ("Calibri, 10"))

#Creating the save to .txt file button
SaveButton = tk.Button(WhiteBackground,
                        text = "Save .txt",
                        width = 10,
                        bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                        relief = "flat",
                        command = TranscriptionTextFile)
SaveButton.grid(column = 0, row = 3, sticky = tk.S, padx = (20,10), pady = (20,10))
SaveButton.config(font = "Calibri 12", fg = "white")

#####################################################################
#tkinter main loop
#####################################################################

window.mainloop()