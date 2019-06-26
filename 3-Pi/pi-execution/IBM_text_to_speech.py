from ibm_watson import TextToSpeechV1
import json
import os
from subprocess import call

#Get ibm-watson(3.0.4) using pip3 : pip3 install ibm-watson
#Ensure aplay is available on the system

text_to_speech = TextToSpeechV1(
    iam_apikey='vR8DQziWtKINmTe51yorcFAcD6rGcuc2LOvcvnY-Xw3U',
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api'
)

predefined_actions = ["I would like a coffee", "I would like to go out", "I would like to go on a bus", "I want to go home", "I am happy today", "Please stand further from me", "Please stand closer to me", "I'm ready"," ","Dinner","Good","Home","No","Sorry"] 
#Add phrase here, audio files are numbered in order of this list

for idx,action in enumerate(predefined_actions):
    with open('audio_files/'+str(idx)+'.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                action,
                voice='en-US_AllisonVoice',
                accept='audio/wav'        
            ).get_result().content)
    os.system('aplay ' + 'audio_files/'+str(idx)+'.wav')

print("Renaming 9.wav to Dinner.wav")
call(["mv", "audio_files/9.wav", "audio_files/Dinner.wav"])
print("Renaming 10.wav to Good.wav")
call(["mv", "audio_files/10.wav", "audio_files/Good.wav"])
print("Renaming 11.wav to Home.wav")
call(["mv", "audio_files/11.wav", "audio_files/Home.wav"])
print("Renaming 12.wav to No.wav")
call(["mv", "audio_files/12.wav", "audio_files/No.wav"])
print("Renaming 13.wav to Sorry.wav")
call(["mv", "audio_files/13.wav", "audio_files/Sorry.wav"])