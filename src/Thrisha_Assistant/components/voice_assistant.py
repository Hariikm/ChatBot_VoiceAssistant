import openai
import os
from pathlib import Path
import speech_recognition as sr
import pyttsx3
import elevenlabs
from elevenlabs import set_api_key as voice_key
from elevenlabs import generate, stream
from elevenlabs import play


class AllCode:

    def get_keys():

        openai_api_key = os.getenv("OpenAI_API")
        elevenlabs_api_key = os.getenv("ElevenLabs_API")

    def run_code():

        Human_voice= True


        voice_key("527a8de70acf2831792101b9b88b0c53")
        key= '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'

        openai.api_key=  key

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
        quit_code= "close the program"

        while True:

            with mic as source:
                print("\nlistening...\n")
                r.adjust_for_ambient_noise(source, duration= 1)
                audio= r.listen(source, timeout=8)       # It waits for 8 seconds for the sound
                print("completed")


                try:
                    user_input= r.recognize_google(audio)
                    print(user_input)

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
            print(f"\n{response}\n")

            if Human_voice:
                    audio = generate(response, voice= "Bella")
                    play(audio)

            else:

                engine.say(f"{response}")
                engine.runAndWait()