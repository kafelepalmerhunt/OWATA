import whisper, os, tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk() #Create the window

window_width = 500
window_height = 250
window_size = str(window_width)+'x'+str(window_height)
window.geometry(window_size)

window.title("OpenAI Whisper Transcription (Base)")
ico = Image.open('Images/TheWhiteDot_Logo.png')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

l = tk.Label(window, text = "OpenAI Whisper Transcription (Base)")
l.config(font = ("Calibri, 12"))
l.pack(side=tk.TOP, anchor=tk.NW, padx=(10,10), pady=(10,10))

T = tk.Text(window, height = 13, width = 75)
T.pack(side=tk.TOP, anchor=tk.NW, padx=(10,10), pady=(10,10))
T.config(font = ("Calibri, 10"))

#Create a blank text file
#f = open("Test2.txt", "w")

#Loads the Whisper model to use for transcription
model = whisper.load_model('base')

#Setting what should be transcribed
result = model.transcribe('Video/Test.mkv', fp16 = False, language="en")

Transcription = (result['text'])
T.insert(tk.END, Transcription)

#Writing the transscribed text
#f.write(result['text'])
#print(result['text'])

#Opens the transcription in notepad
#os.startfile('Test2.txt')

window.mainloop()