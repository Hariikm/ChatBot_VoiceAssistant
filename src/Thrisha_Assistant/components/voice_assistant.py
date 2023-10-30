import openai
import os
from pathlib import Path
import speech_recognition as sr
import pyttsx3
import elevenlabs
from elevenlabs import set_api_key as voice_key
from elevenlabs import generate, stream
from elevenlabs import play
from Thrisha_Assistant.components import APIKeys
from Thrisha_Assistant import logger
from Thrisha_Assistant.utils import read_yaml


settings= read_yaml(Path("settings.yaml"))


key_var= APIKeys()
key_var.get_keys()
openai_api_key= key_var.openai_api_key
elevenlabs_api_key= key_var.elevenlabs_api_key


class AllCode:

    def run_code():

        speak_limit = settings.speak_limit

        Human_voice= settings.Human_voice


        voice_key(elevenlabs_api_key)

        openai.api_key=  openai_api_key

        personality= Path("personality.txt")

        with open(personality, 'r') as file:
            mode= file.read()

        messages= [
            {"role":"system", "content": f"{mode}"}
        ]

        # Using pyttsx3
        engine= pyttsx3.init()
        voices= engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)   #1 is for female


        r= sr.Recognizer()
        mic= sr.Microphone(device_index=0)   # Here 0 is default microphone and wored best for me, You can play with this in trials.ipynb
        r.dynamic_energy_threshold= True
        # r.energy_threshold= 600           # If the energy threshold is False, then uncommand this.
        quit_code= settings.quit_code
        quit_code= quit_code

        while True:

            with mic as source:
                print("\nlistening...\n")
                r.adjust_for_ambient_noise(source, duration= 1)
                timeout= settings.listen_timeout
                audio= r.listen(source, timeout=timeout)       # It waits for 8 seconds for the sound
                print("completed")


                try:
                    user_input= r.recognize_google(audio)
                    logger.info(f"\nUser input: {user_input}\n")

                    if quit_code in user_input.lower():
                        print("\nExiting the program.\n")
                        break

                except:
                    print("Didn't received any inputs")
                    continue

            messages.append({"role":"user", "content": user_input})


            completion= openai.ChatCompletion.create(
                model= "gpt-3.5-turbo-0301",
                messages= messages,
                temperature= 0.8
            )


            response= completion.choices[0].message.content
            messages.append({"role":"assistant", "content": response})
            response_length= len(response.split())

            
            max_legth= settings.max_length_to_speak
            warning= settings.max_length_warning


            if Human_voice:

                if speak_limit and response_length>max_legth:
                    logger.info(f"\n{response}\n")
                    audio = generate(warning, voice= "Bella")
                    play(audio)

                else:
                    logger.info(f"\n{response}\n")
                    audio = generate(response, voice= "Bella")
                    play(audio)

            else:

                if speak_limit and response_length>max_legth:
                    logger.info(f"\n{response}\n")
                    engine.say(f"{response}")
                    engine.runAndWait()

                else:
                    logger.info(f"\n{response}\n")
                    engine.say(f"{response}")
                    engine.runAndWait()