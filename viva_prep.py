import os
import streamlit as st
import speech_recognition as sr
import cohere
import pyttsx3
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from io import BytesIO


# Set environment variable to suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["OPENAI_API_KEY"] = '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'

# Load the necessary models
co = cohere.Client("G73sHe2ITKfFitJHFJNJR61gWIwxWjQzOc2wqNk3")
bo = cohere.Client("095qHCKCNMIcXbLQHkwKZisE7QUGgttcs7qj44fi")
# template = """Question: {question}
# Answer: """
# prompt = PromptTemplate.from_template(template)
# llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"],temperature=0)
# llm_chain = LLMChain(prompt=prompt,llm=llm,verbose=True)
# print(llm_chain.run("hello"))

# Function to start the viva preparation
def start_viva_preparation(subject):
    preamble = f"You are the engineering viva examiner and I'm the candidate. Follow these instructions: You are an Engineering Viva preparation bot for the respective subject: {subject}. Ask me questions based on the subject in a conversational manner. Ask a maximum upto 7 questions."
    
    # Clear chat history
    chat_history = []

    def send_prompt_and_get_response(prompt):
        chat_history.append({"role": "user", "message": prompt})
        response = co.chat(
            temperature=0.3,
            message=prompt,
            preamble=preamble,
            chat_history=chat_history,
            return_prompt=True
        )
        chat_history.append({"role": "bot", "message": response.text})
        return response

    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Start the viva preparation
    st.write("Say 'End' to stop the interview")
    response = send_prompt_and_get_response("Hello")
    st.write(response.text)
    engine.say(response.text)
    engine.runAndWait()

    for i in range(100):
        # Use SpeechRecognition to recognize speech input
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio)
            st.write("You:", user_input)
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand what you said.")
            continue
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
            continue

        # if not user_input:
        #     break

        response = send_prompt_and_get_response(user_input)
        if response=="end":
            st.write("The Viva has ended")
            break
        else:
            st.write("Bot:", response.text)
            engine.say(response.text)
            engine.runAndWait()

    pre =(f"Act as Feedback Generator and give accurate feedback for the response{chat_history}")
    final=f"Go through the {chat_history} which is a conversation between an Engineering Viva examiner and candidate.Take the {chat_history} Give a feedback how the user has performed, and answers accuracy also give an overall rating out of 10 which is based on the {chat_history}"
    res = bo.chat(
            temperature=0.3,
            message=final,
            preamble=pre,
            chat_history=chat_history,
            return_prompt=True
        )
    st.write(res)
        
        # Here you might want to check if user_input contains "end" or some other command to terminate the conversation
        # and then break out of the loop accordingly

# Streamlit UI
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Engineering Viva Preparation Bot</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #FFFFFF;'>", unsafe_allow_html=True)

# Ask the user for the subject
subject = st.text_input("Enter the Engineering Subject:", "Electrical Engineering")

# Add some space before the button
st.write('<br><br>', unsafe_allow_html=True)

if st.button("Start Viva Preparation"):
    start_viva_preparation(subject)
