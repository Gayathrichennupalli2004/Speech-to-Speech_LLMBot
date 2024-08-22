from flask import Flask, render_template, jsonify
import threading
import cv2
import speech_recognition as sr
import pyttsx3
import openai

app = Flask(__name__)

# Step 1: Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return ""
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return ""

# Step 2: LLM Response Generation
# Using a mock response function for now
def generate_response_mock(prompt):
    return "This is a mock response to your input: " + prompt

# Optionally, you can use OpenAI's GPT-3 (requires API key)
def generate_response(prompt):
    openai.api_key = 'G7SsN8ygZZE9P4yVFATdeA2eOI3TBIke'  # Replace with your OpenAI API key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Step 3: Text-to-Speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Step 4: Webcam Capture
def capture_webcam():
    cap = cv2.VideoCapture(0)  # Open the default webcam

    if not cap.isOpened():
        print("Error: Webcam not found or not accessible.")
        return

    print("Webcam is working. Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                print("Error: Failed to capture image.")
                break

            cv2.imshow('Webcam Test', frame)  # Display the frame

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        cap.release()  # Release the capture
        cv2.destroyAllWindows()  # Close all OpenCV windows

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/start_listening')
def start_listening():
    def background_task():
        user_input = recognize_speech()
        if user_input:
            response = generate_response_mock(user_input)  # Replace with generate_response(user_input) for real LLM
            speak_text(response)
    
    threading.Thread(target=background_task).start()
    return jsonify({"status": "Listening started"})

@app.route('/open_webcam')
def open_webcam():
    threading.Thread(target=capture_webcam).start()
    return jsonify({"status": "Webcam opened"})

if __name__ == "__main__":
    app.run(debug=True)
