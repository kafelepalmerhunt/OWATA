import whisper, os, tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import timedelta

####################################################################
#Varibles
####################################################################

filename = ""
Transcription = ""
AppName = "OWATA.ai"
#AppDescription = "OpenAI Whisper Transcription App"

PrimaryColour = "#73c9d3" #Blue
SecondaryColour = "#dddddd" #Light Grey

##################################################################
#Window Initalistion
#################################################################

#Creating the window and setting the properties
window = tk.Tk() 
window_width = 725 #pixels
window_height = 425 #pixels
window_size = str(window_width) + 'x' + str(window_height)
window.geometry(window_size)
window.resizable(width = False, height = False)

#Adding the window title and icon
window.title(AppName)
ico = Image.open('Images/OWATA_LOGO.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

#########################
#Creating the window tabs
#########################

#Widget that manages the collection of tab windows
notebook = ttk.Notebook(window)

#Creating the frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

#Adds the tabs to the notebook
notebook.add(tab1, text = "File Transcription")
notebook.add(tab2, text = "Live Transcription")
notebook.grid(column=0, row=1)

####################################################################
#Functions
####################################################################

#Restting the app to create a new transcription
def NewTranscription():
    #Add codehere
    return

#Cutting any selected text in the app
def CutText():
    return

#Copying any selected text in the app
def CopyText():
    return

#Pasting any selected text in the app
def PasteText():
    return

#Adding the file and path to be transcribed
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

#Transcribes the file from the selected path
def transcribefile(filename):
    
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

#Saves the transcribbed text as a .txt file (notepad)
def OpenTranscriptionTextFile():
    
    #Create a blank text file
    #f = open("Test2.txt", "w")

    #Writing the transscribed text
    #f.write(Transcription.strip())

    #Opens the transcription in notepad
    os.startfile('TextFiles\Transcription.txt')


def transcribe_audio(path):
    
    #Deletes any existing text in the transcription box
    T.delete("1.0", tk.END)

    model = whisper.load_model("base") # Change this to your desired model
    #print("Whisper model loaded.")
    transcribe = model.transcribe(audio = path, fp16 = False, language="en")
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+'.000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+'.000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        TextFilename = os.path.join("TextFiles", f"Transcription.txt")
        with open(TextFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

            #Adds the new transcription to the box and removes the space at the front via strip
            T.insert(tk.END, segment.strip() + '\n\n')

    return TextFilename

###################################################################
#Creating the menubar
###################################################################

#Creating the menubar which contains the top level menu buttons
menubar = tk.Menu(window)
window.config(menu = menubar)

#Creating the file menu button and all options inside it
fileMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label = "File", menu = fileMenu)
fileMenu.add_command(label = "New Transcription", command = NewTranscription)
fileMenu.add_command(label = "Open Transcription as .txt", command = OpenTranscriptionTextFile )
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = quit)

#Creating the edit menu button and all options inside it
editMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label = "Cut", command = CutText)
editMenu.add_command(label = "Copy", command = CopyText)
editMenu.add_command(label = "Paste", command = PasteText)

#Creating the whisper button and all options inside it
whisperMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Whisper", menu = whisperMenu)

#Creating the view menu button and all options inside it
viewMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label = "View", menu = viewMenu)

#Creating the help menu button and all options inside it
helpMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Help", menu = helpMenu)

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
WhiteBackground = tk.Frame(tab1,
                            bg = SecondaryColour,
                            width = window_width,
                            height = (window_height))
WhiteBackground.grid(column = 0, row = 0, sticky = tk.NW, columnspan = 1, padx = (0,0), pady = (0,1))
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
                             command = lambda : transcribe_audio(filename))
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
                        text = "Open .txt",
                        width = 10,
                        bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                        relief = "flat",
                        command = OpenTranscriptionTextFile)
SaveButton.grid(column = 0, row = 3, sticky = tk.S, padx = (20,10), pady = (20,10))
SaveButton.config(font = "Calibri 12", fg = "white")

#####################################################################
#tkinter main loop
#####################################################################

window.mainloop()