from ibm_watson import TextToSpeechV1
import json
import os

#Get ibm-watson(3.0.4) using pip3 : pip3 install ibm-watson
#Ensure aplay is available on the system

text_to_speech = TextToSpeechV1(
    iam_apikey='vR8DQziWtKINmTe51yorcFAcD6rGcuc2LOvcvnY-Xw3U',
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api'
)

predefined_actions = ["Good", "No", "Sorry", "Dinner", "Home"]

for action in predefined_actions:
	with open('audio_files/'+action+'.wav', 'wb') as audio_file:
	    audio_file.write(
	        text_to_speech.synthesize(
	            action,
	            voice='en-US_AllisonVoice',
	            accept='audio/wav'        
	        ).get_result().content)
	os.system('aplay ' + 'audio_files/'+action+'.wav')
