import whisper
import os

#Create a blank text file
f = open("Test2.txt", "w")

#Loads the Whisper model to use for transcription
model = whisper.load_model('base')

#Setting what should be transcribed
result = model.transcribe('Video/Test.mkv', fp16 = False, language="en")

#Writing the transscribed text
f.write(result['text'])
print(result['text'])

#Opens the transcription in notepad
os.startfile('Test2.txt')