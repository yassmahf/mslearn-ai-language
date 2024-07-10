from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces

import azure.cognitiveservices.speech as speech_sdk



def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(
        subscription=ai_key,
        region=ai_region)
         
        translation_config.speech_recognition_language = 'en-US'
 
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi')
 
        print('Ready to translate from', translation_config.speech_recognition_language)


        # Configure speech
        
        speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)



        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech
 
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_config)
 
    print("Speak now...")
 
    result = translator.recognize_once_async().get()
 
    if result.reason == speech_sdk.ResultReason.TranslatedSpeech:
     print('Translating "{}"'.format(result.text))
   
     for language, translation in result.translations.items():
        print('Translation in {}: {}'.format(language, translation))
    else:
     print("No speech could be recognized or translation failed.")


    # Synthesize translation
    
    voices = {
    "fr": "fr-FR-HenriNeural",
    "es": "es-ES-ElviraNeural",
    "hi": "hi-IN-MadhurNeural"
    }
    translation = "Bonjour tout le monde"
 
 
    # Set the speech synthesis voice name based on the target language
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
 
    # Initialize the speech synthesizer
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
 
    # Synthesize the translated text to speech
    speak = speech_synthesizer.speak_text_async(translation).get()
 

    # Check if the synthesis was successful
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
      print(speak.reason)
    else:
      print("Speech synthesis completed successfully.")






if __name__ == "__main__":
    main()