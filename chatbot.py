import pyttsx3
import speech_recognition as sr
import time
import openai

# OpenAI Configuration
openai.api_key = "sk-your-api-key-here"  # Replace with your actual API key


# Initialize TTS Engine with Female Voice
def setup_voice_engine():
    engine = pyttsx3.init()

    # Get available voices and select the best female option
    voices = engine.getProperty('voices')

    # Prefer "Zira" (Windows) or "Karen" (macOS) if available
    female_voices = [v for v in voices if "female" in v.name.lower() or "zira" in v.name.lower()]

    if female_voices:
        engine.setProperty('voice', female_voices[0].id)
    else:
        # If no female voice is found, try setting a specific female voice ID
        for voice in voices:
            if voice.id == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0":
                engine.setProperty('voice', voice.id)
                break
            elif voice.id == "com.apple.speech.synthesis.voice.karen":
                engine.setProperty('voice', voice.id)
                break
        print("Warning: No female voice found - using default voice")

    # Voice customization
    engine.setProperty('rate', 165)  # Speech speed
    engine.setProperty('volume', 0.9)  # Volume (0-1)
    return engine


engine = setup_voice_engine()


def elsa_speak(text):
    print(f"Elsa : {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise with a longer duration
        r.adjust_for_ambient_noise(source, duration=2)

        audio = r.listen(source, phrase_time_limit=5)  # Set a time limit for listening

    try:
        command = r.recognize_google(audio)
        print(f"You : {command}")
        return command.lower()
    except sr.UnknownValueError:
        elsa_speak("Sorry Sammy, I couldn't understand what you said.")
    except sr.RequestError as e:
        elsa_speak("Sorry Sammy, I couldn't connect to the speech recognition service.")
        print(f"Error: {e}")
    except Exception as e:
        elsa_speak("Sorry Sammy, something went wrong.")
        print(f"Error: {e}")
    return ""


# Main Loop
elsa_speak("Good Afternoon Sammy! I am Elsa, your personal assistant. How can I help you today?")

while True:
    query = listen()

    if 'hello' in query:
        elsa_speak("Hello Sammy! Hope you're having a great day.")

    elif 'how are you' in query:
        elsa_speak("I'm always good when I'm talking to you.")

    elif 'your name' in query:
        elsa_speak("I'm Elsa. Your virtual humanoid assistant.")

    elif 'bye' in query or 'exit' in query or 'quit' in query:
        elsa_speak("Goodbye Sammy! Take care.")
        break

    elif 'ask openai' in query:
        try:
            prompt = query.replace('ask openai', '').strip()
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=200
            )
            elsa_speak(response.choices[0].text)
        except Exception as e:
            elsa_speak("Sorry, I couldn't get a response from OpenAI.")
            print(f"Error: {e}")

    elif query != "":
        elsa_speak("Hmm, I'm still learning that.")

    time.sleep(1)  # Small pause before listening again
