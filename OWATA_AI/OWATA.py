import whisper, os, tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from datetime import timedelta

####################################################################
#Varibles
####################################################################

filename = ""
Transcription = ""
AppName = "OWATA"

PrimaryColour = "#73c9d3" #Blue
PrimaryColour2 = "#6dbbc4" #Blue - slightly darker
SecondaryColour = "#dddddd" #Light Grey
SecondaryColour2 = "#808080" #Light Grey - slightly darker

Transcribing = False

#For iterating the text output file number
i = 0

##################################################################
#Window Initalistion
#################################################################

#Creating the window and setting the properties
window = tk.Tk() 
window_width = 725 #pixels
window_height = 400 #pixels
window_size = str(window_width) + 'x' + str(window_height)
window.geometry(window_size)
window.resizable(width = False, height = False)

#Adding the window title and icon
window.title(AppName)
window.iconbitmap('OWATA_ICON.ico')

#Creating the inital console spew
g = 0
if g == 0:
    print("OWATA - OpenAI Whisper Transcription App")
    print("App Version 1.0.0 - Python Version 3.10.6")
    print("Whisper is a general-purpose speech recognition model")
    print("For more information - https://github.com/openai/whisper")
    print("Base Model - Size 74MB - Required Vram ~1GB")
    print("Created by Kafele Jabari Palmer-Hunt - 2023")
    print("--------------------------------------------------------")
    g += 1

#########################
#Creating the window tabs
#########################

# Create an instance of ttk style
style = ttk.Style()
style.theme_create('Cloud', settings={
    ".": {
        "configure": {
            "background": SecondaryColour,
             "borderwidth" : 0,
              "relief" : "flat" # All colors except for active tab-button
        }
    },
    "TNotebook": {
        "configure": {
            "background": PrimaryColour, # color behind the notebook
            "tabmargins": [5, 5, 0, 0],
             "borderwidth" : 0 # [left margin, upper margin, right margin, margin beetwen tab and frames]
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "focuscolor": {"configure" : {"."}},
            "background": PrimaryColour2,
             "foreground" : "white", # Color of non selected tab-button
            "padding": [20, 1], # [space beetwen text and horizontal tab-button border, space between text and vertical tab_button border]
        },
        "map": {
            "background": [("selected", SecondaryColour)],
             "foreground": [("selected", SecondaryColour2)], # Color of active tab
            "expand": [("selected", [1, 1, 1, 0])] # [expanse of text]
        }
    }
})

style.theme_use('Cloud')

#Widget that manages the collection of tab windows
notebook = ttk.Notebook(window)

#Creating the frames for each tab
tab1 = ttk.Frame(notebook, borderwidth=0)

#Adds the tabs to the notebook
notebook.add(tab1, text = "File Transcription")
notebook.grid(column=0, row=1)

####################################################################
#Functions
####################################################################

#Adding the file and path to be transcribed
def OpenFile():
    
    print("Called Function OpenFile")

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
    TranscriptionTextbox.delete("1.0", tk.END)

    return input_path, filename, setfilename

#Transcribes the file from the selected path
def TranscribeFile(filename):
    
    #Loads the Whisper model to use for transcription
    model = whisper.load_model('base')

    #Setting what should be transcribed
    result = model.transcribe(filename, fp16 = False, language="en")

    #Making the var global to be accessed/changed in other places
    global Transcription

    #Setting the var transcription as the result of the model.transcribe method
    Transcription = (result['text'])
    
    #Deletes any existing text in the transcription box
    TranscriptionTextbox.delete("1.0", tk.END)

    #Adds the new transcription to the box and removes the space at the front via strip
    TranscriptionTextbox.insert(tk.END, Transcription.strip())

    print("Called Function TranscribeFile")

    return result, Transcription

#Saves the transcribed text as a .txt file (notepad)
def OpenTranscriptionTextFile():
    
    #Opens the transcription in notepad
    global i
    
    #Opens the text file
    os.startfile('Transcription%s.txt' % i)

    print("Called Function OpenTranscriptionTextFile " + str(Transcribing))
    print("Opening Text File " + 'Transcription%s.txt' % i)

def TranscribeAudio(path):
    
    global i
    while os.path.exists('Transcription%s.txt' % i):
        i += 1

    global Transcribing
    Transcribing = True

    print("Called Function TranscribeAudio")
    print("Transcribing Audio File - " + str(filename))

    #Deletes any existing text in the transcription box
    TranscriptionTextbox.delete("1.0", tk.END)

    model = whisper.load_model("base")
    transcribe = model.transcribe(audio = path, fp16 = False, language="en")
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+'.000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+'.000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        TextFilename = os.path.join("Transcription%s.txt" % i)
        with open(TextFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

            #Adds the new transcription to the box and removes the space at the front via strip
            TranscriptionTextbox.insert(tk.END, segment.strip() + '\n\n')

    print("Transcription Complete")
    
    return TextFilename, Transcribing

def ResetAll():
    
    TranscriptionTextbox.delete("1.0",tk.END)
    input_entry.delete("0",tk.END)

    print("Called Function ResetAll")
    print("Resetting Application")


####################################################################
#Drawing the interface button and text etc.
####################################################################

#Creating the blue background at the top
HeadingFrame = tk.Frame(window,
                            bg = PrimaryColour,
                            width = window_width,
                            height = 60,
                            borderwidth = 0
                            )
HeadingFrame.grid(column = 0, row = 0, sticky = tk.NW, columnspan = 1, padx = (0,0), pady = (0,0))
HeadingFrame.grid_propagate(0)

#Creating the gey background for the main body
BodyFrame = tk.Frame(tab1,
                            bg = SecondaryColour,
                            width = window_width,
                            height = window_height,
                            borderwidth = 0
                            )
BodyFrame.grid(column = 0, row = 0, sticky = tk.NW, columnspan = 1, padx = (0,0), pady = (0,1))
BodyFrame.grid_propagate(0)

#Creating the Main Label
MainTitle = tk.Label(HeadingFrame,
             text = AppName)
MainTitle.config(font ="Calibri 32 bold", bg = PrimaryColour, fg = "white")
MainTitle.grid(column = 0, row = 0, sticky = tk.NE, columnspan = 1, padx = (10,10), pady = (1,1))

#Creating the open file button in the window
OpenFileButton = tk.Button(BodyFrame, 
                            text = "Browse",
                            width = 10,
                            bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                            relief = "flat",
                            command = OpenFile)
OpenFileButton.grid(column = 0, row = 2, sticky = tk.NW, padx = (20,10), pady = (20,10))
OpenFileButton.config(font = "Calibri 10", fg = "white")

#Drawing the file path
input_entry = tk.Entry(BodyFrame,
                        text = "", 
                        width = 80)
input_entry.grid(column = 1, row = 2, sticky = tk.W, padx = (10,10), pady = (20,10))
input_entry.config(font = ("Calibri, 10"))



#Creating the transcribe button in the window
TranscribeButton = tk.Button(BodyFrame,
                                text  ="Transcribe",
                                width = 10,
                                bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                                relief = "flat",
                                command = lambda : TranscribeAudio(filename))

TranscribeButton.grid(column = 0, row = 3, sticky = tk.NW, padx = (20,10), pady = (20,10))
TranscribeButton.config(font = "Calibri 10", fg = "white")

#Creating the transcription text window
TranscriptionTextbox = tk.Text(BodyFrame,
            height = 13, 
            width = 80, 
            relief = "groove")
TranscriptionTextbox.grid(column = 1 , row = 3, rowspan=4, sticky = tk.NW, padx = (10,10), pady = (10,10))
TranscriptionTextbox.config(font = ("Calibri, 10"))

#Creating the save to .txt file button
OpenButton = tk.Button(BodyFrame,
                        text = "Open .txt",
                        width = 10,
                        bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                        relief = "flat",
                        command = OpenTranscriptionTextFile)
OpenButton.grid(column = 0, row = 3, sticky = tk.NW, padx = (20,10), pady = (50,10))
OpenButton.config(font = "Calibri 10", fg = "white")


#Creating the reset all button
ResetAllButton = tk.Button(BodyFrame,
                        text = "Reset All",
                        width = 10,
                        bg = PrimaryColour, activebackground = "black", activeforeground = "white",
                        relief = "flat",
                        command = ResetAll)
ResetAllButton.grid(column = 0, row = 3, sticky = tk.NW, padx = (20,10), pady = (190,10))
ResetAllButton.config(font = "Calibri 10", fg = "white")


#####################################################################
#Tkinter Main Loop
#####################################################################

window.mainloop()