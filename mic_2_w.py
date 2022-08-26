import time
import json
#import os
import azure.cognitiveservices.speech as speechsdk
recog=""
def speech_recognize_continuous_async_from_microphone():
    """performs continuous speech recognition asynchronously with input from microphone"""
    speech_config = speechsdk.SpeechConfig(subscription="8c393570a0ce4dde9c5429fd6ab4357c", region="uksouth")
    # The default language is "en-us".
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        global recog
        print('RECOGNIZING: {}'.format(evt))
        
        recog+=" "+evt.result.text.split()[-1]
        print("----------------------------------------------")
        print(recog)
        print("------------------------------------------------")

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZED: {}'.format(evt))
        
  

    def stop_cb(evt: speechsdk.SessionEventArgs):
        global recog
        """callback that signals to stop continuous recognition"""
        print('CLOSING on {}'.format(evt))      
        nonlocal done
        done = True
    
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
    # Other tasks can be performed on this thread while recognition starts...
    # wait on result_future.get() to know when initialization is done.
    # Call stop_continuous_recognition_async() to stop recognition.
    result_future = speech_recognizer.start_continuous_recognition_async()

    result_future.get()  # wait for voidfuture, so we know engine initialization is done.
    print('say something.')

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
        #print('type "stop" then enter when done')
        if ("stop" in recog):
           
            print('Stopping async recognition.')
            speech_recognizer.stop_continuous_recognition_async()
            break
    
    print("recognition stopped, main thread can exit now.")
    return recog
speech_recognize_continuous_async_from_microphone()