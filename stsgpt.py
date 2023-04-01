import openai
import speech_recognition as sr
import pyttsx3
import time 
import re

from playsound import playsound
from gtts import gTTS

def stop_program(transcription):
    pattern = re.compile(r'\bSTOP!\b', re.IGNORECASE)
    return bool(pattern.search(transcription))

# Initialize OpenAI API

openai.api_key = "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"

# Initialize the text to speech engine 

engine=pyttsx3.init()





def transcribe_audio_to_test(filename):

    recogizer=sr.Recognizer()

    with sr.AudioFile(filename)as source:

        audio=recogizer.record(source) 

    try:

        return recogizer.recognize_google(audio)

    except:
        speak_text("There has been some unknown errors, please try again!")
        print("skipping unkown error")



def generate_response(prompt):

    response= openai.Completion.create(

        engine="text-davinci-003",

        prompt=prompt,

        max_tokens=4000,

        n=1,

        stop=None,

        temperature=0.5,

    )

    return response ["choices"][0]["text"]

def speak_text(text):

    engine.say(text)

    engine.runAndWait()



def main():

    while True:

        # Wait for user to say "hello"
        print("Hey! This is Akash, say hello! to ask me anything!")
        speak_text("Hey! This is Akash, say hello to ask me anything!")

        with sr.Microphone() as source:

            recognizer=sr.Recognizer()

            audio=recognizer.listen(source)

            try:

                transcription = recognizer.recognize_google(audio)

                if stop_program(transcription):
                    print('Program stopped by user')
                    speak_text('Program stopped by user')
                    break

                if transcription.lower()=="hello":

                    #record audio

                    filename ="input.wav"

                    speak_text("Say your question") 
                    print("Say your question")

                    with sr.Microphone() as source:

                        recognizer=sr.Recognizer()

                        source.pause_threshold=1

                        audio=recognizer.listen(source,phrase_time_limit=5,timeout=None)

                        with open(filename,"wb")as f:

                            f.write(audio.get_wav_data())

                

                    #transcript audio to test 

                    text=transcribe_audio_to_test(filename)

                    if text:
                        speak_text(f"you said : {text}")
                        print(f"you said : {text}")
                        
                        

                        #Generate the response

                        response = generate_response(text)

                        print(f"chat gpt 3 says: {response}")
                        speak_text(f"chat gpt 3 says: {response}")

                        tts = gTTS(text=response, lang='en')

                        tts.save("sample.mp3")

                        # playsound("sample.mp3")   

                        #read resopnse using GPT3

                        speak_text(response)

            except Exception as e:

                

                print("An error ocurred : {}".format(e))
                speak_text("An error ocurred : {}".format(e))

if __name__=="__main__":

    main()
