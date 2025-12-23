import init as i
import tensorflow
import streamlit as st
import PyPDF2
import spacy
import en_cv_info_extr
from sklearn import *
import speech_recognition as sr
import pyttsx3
import comtypes

from io import BytesIO


comtypes.CoInitialize()


nlp = spacy.load("en_cv_info_extr")
nlp = en_cv_info_extr.load()
bo=i.bo
co=i.co
template=i.template
prompt=i.prompt
llm=i.llm
llm_chain=i.llm_chain
print(llm_chain.run("hello"))

def extraction(text):
    doc = nlp(text)
    technical_skills = []
    languages = []

    for ent in doc.ents:
        if ent.label_ == "HSKILL":
            technical_skills.append(ent.text)
        elif ent.label_ == "language":
            languages.append(ent.text)

    return technical_skills, languages

# Function to read skills from PDF
def read_pdf(uploaded_file):
    technical_skills = []
    with BytesIO(uploaded_file.read()) as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            skills, _ = extraction(text)
            technical_skills.extend(skills)
    return technical_skills

# Function to start the interview
def start_interview(pdf_file_path, user_name, user_position):
    user_skills = read_pdf(pdf_file_path)
    st.write(f"Skills extracted from PDF: {user_skills}")
    st.write()
    st.write("Please Say 'Thank You' to end the interview")
    st.write()
    preamble = ("Pretend you are an interviewer for a company and I am the interview candidate."
                f"The position I've applied for is: {user_position} and my skills are {user_skills}"
                f"Follow these instructions: I have come to you for an interview, and my name is {user_name}."
                "Now ask me a question to get started with my interview. "
                "Ask me questions based on my skills only 1 question at a time"
                "You can abort this interview after four to six questions and end the interview after that. "
                "If you think my interview response is good, you can select me for the job, "
                "and if not, you can reject my application.")
    
    # Clear chat history
    chat_history = []

    def prompting(prompt):
        chat_history.append({"role": "candidate", "message": prompt})
        response = co.chat(
            temperature=0.3,
            message=prompt,
            preamble=preamble,
            chat_history=chat_history,
            return_prompt=True
        )
        chat_history.append({"role": "interviewer", "message": response.text})
        return response

    # Function to listen for user's response
    def listen_for_response():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
        try:
            user_response = recognizer.recognize_google(audio)
            st.write("User said:", user_response)
            return user_response
        except sr.UnknownValueError:
            st.write("Speech recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    # Function to speak the response
    def speak_response(response_text):
        engine = pyttsx3.init()
        engine.say(response_text)
        engine.runAndWait()

    # Start the interview
    response = prompting(f"Hi there, My name is {user_name}")
    st.write(response.text)
    speak_response(response.text)
    for i in range(100):
        user_response = listen_for_response()
        if user_response == "thank you":
            st.write("The Interview has ended")
            st.write()
            break
        if user_response is not None:
            response = prompting(user_response)
            st.write(response.text)
            speak_response(response.text)
        else:
            st.write("Sorry, I didn't get that. Can you repeat that again?")
            speak_response("Sorry, I didn't get that. Can you repeat that again?")
    pre =(f"Act as Feedback Generator and give accurate feedback for the response{chat_history}")
    final=f"Go through the {chat_history} which is a conversation between an interviewer and candidate.Take the {chat_history} Give a feedback how the user has performed, analysing his speaking skills and answers accuracy also tell whether is he fit for the particular job description of {user_position} and give an overall rating out of 10 which is based on the {chat_history}"
    res = llm_chain.run(f'{pre} {final}')
    # speak_response(res.text)
    # st.write(chat_history)
    st.write("Here is a Feedback on how you performed")
    st.write()
    st.write(res)


# Streamlit UI
st.set_page_config(layout="wide")
# st.title("Voice Chatbot Interview")
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>SADHANA</h1>", unsafe_allow_html=True)

# Add some space between the title and the content
st.write('<br>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #FFFFFF;'>", unsafe_allow_html=True)

st.write('<form action="/process" method="post" enctype="multipart/form-data">', unsafe_allow_html=True)

user_name=st.text_input("Name", key="name")
user_position=st.text_input("Position", key="position")
pdf_file_path = st.file_uploader("Upload your CV (PDF file):")

st.write('</form>', unsafe_allow_html=True)
# st.write('</footer>', unsafe_allow_html=True)

# Add more space before the button
st.write('<br><br>', unsafe_allow_html=True)

if st.button("Start Interview"):
    if pdf_file_path is not None:
        start_interview(pdf_file_path, user_name, user_position)
    else:
        st.write("Please upload your CV first.")

# Uninitialize COM when done
comtypes.CoUninitialize()
