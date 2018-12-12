import speech_recognition as sr


def listen_sentence_from_mic(recognizer, microphone):
    """Listen audio input from the user and check for errors.

    This function will check if the instances are from correct classes
    and will capture the audio input from the default microphone of your
    machine. This audio is sent to the Google API and then we check if
    the request was successful or not and if the audio could be translated
    or not.

    Parameters
    ----------
    recognizer : sr.Recognizer
        Recognizer instance from the SpeechRecognition module.
    microphone : sr.Microphone
        Microphone instance from the SpeechRecognition module.

    Returns
    -------
    dict
        a dictionary containing information about the response (e.g.
        if it was a success or not, if there was an error and the
        audio converted to text).
    """

    # Check if instances are from correct class
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    # Record audio from default microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Create response for easy debugging
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # Tries to extract text from audio
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "Could not connect with API."
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Could not understand the instruction."

    return response


# List of sentences accepted
SENTENCES = [
    "kitchen on", "kitchen off", "living room on", "living room off",
    "bathroom on", "bathroom off", "all on", "all off"
]

# Create Recognizer and Mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def get_options():
    """Show which are the current sentences supported by the application.

    Returns
    -------
    str
        a string containing all the sentences supported.
    """

    # Format the available options
    options = (
        "\nHouse Automaton actually supports those sentences:\n"
        "{sentences}\n"
        "\n\nSay something: \n"
    ).format(sentences=', \n'.join(SENTENCES))
    return options
