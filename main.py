import streamlit as st
import json
import os
from streamlit_option_menu import option_menu
# import whisper
from PIL import Image
from gemini_utility import (generate_image,load_gemini_pro_model,gemini_pro_vision_response,embedding_model_response,gemini_pro_response,text_to_speech,speech_to_text)


# accessing the working_directory 
working_directory = os.path.dirname(os.path.abspath(__file__))
# print(working_directory)
# import openai
# import urllib.request 

# configuring openai api key --
config_data = json.load(open(f"{working_directory}/config.json"))
OPEN_AI_KEY = config_data["OPENAI_API_KEY"]
# setting up the page configuration 
st.set_page_config(
    page_title = "OnlyAI",
    page_icon = "🧠",
    layout = "centered"
)

# logo_url = "owner.jpg"
# st.image(logo_url,width=51)
# st.video()
# video_file = open('We.mp4', 'rb')
# video_bytes = video_file.read()
# st.video(video_bytes)
# st.video("We.mp4", format="video/mp4", start_time=0,*, subtitles=None, end_time=None, loop=True, autoplay=True, muted=True)

with st.sidebar:

    selected = option_menu(menu_title="We're OnlyAI!",options=["GPT","Image Generation","Image Captioning","Text-to-Speech","Speech-to-Text","ChatBot","Embed text","About Me"],menu_icon= 'robot',icons=['question-diamond','file-image-fill','card-image','mic-fill','mic','chat-dots-fill','card-text','person-workspace'],default_index=0)


# function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

# About us page 
if selected=="About Me":
    col1,col2 = st.columns(2)
    image = Image.open("owner.jpg")
    with col1 :
            resized_image = image.resize((800,800))
            st.image(image)

    with col2 :
        st.info("Heyy folks! Its me <Himanshu Prajapati> , a final year undergrad at IIT Delhi pursuing Btech. in Electrical Engineering. This is my Streamlit project to make all popular AIs developed by Google , OpenAI and others , available at a single place. I'll keep it updating time to time . Just don't Forget to pin this project in your browser :)")
        st.info("Meanwhile You can also check the other projects developed by me. Thank You!")
        col3,col4 = st.columns(2)
        with col3 :
            st.page_link("https://cgpathway.wixsite.com/sort",label="<CGPAthway>",use_container_width=250)
            # st.button(label="<CGPAthway>",on_click="https://cgpathway.wixsite.com/sort")
        with col4 :
            st.page_link("http://www.azureiitd.com/",label="<Azure>",use_container_width=250)
            # st.button(label="<Azure>",on_click="http://www.azureiitd.com/")

        
# chatbot page //
if selected=="ChatBot":
    model = load_gemini_pro_model()

    # Initialize chat session with streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title 
    st.title("🧠 ChatBot")

    # display the chat history //
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    # input title for user's message /
    user_prompt = st.chat_input("Ask OnlyAI.... ")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display gemini pro response //
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# image generation //
if selected=="Image Generation" :
    # streamlit page title 
    st.title("⏳ Image Generator ")
    # text input for image generation prompt 
    img_description = st.text_input('Image Description')

    if st.button("Generate Image"):
        generated_image = generate_image(img_description)
        st.image(generated_image)

# image captioning page 
if selected=="Image Captioning" :
    # model = gemini_pro_vision_response()
    # streamlit page title 
    st.title("📷 Snap Narrate")
    uploaded_image = st.file_uploader("Upload an image ...",type=["jpg","jpeg","png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)
        col1,col2 = st.columns(2)
        with col1 :
            resized_image = image.resize((800,500))
            st.image(resized_image)
        default_prompt = "write a short caption for this image"

        # getting the response from gemini_pro_vision_model
        caption = gemini_pro_vision_response(default_prompt,image)

        with col2 :
            st.info(caption)

# text embedding page 
if selected=="Embed text":
    st.title("<> Embed Text")

    # input text box 
    input_text = st.text_area(label="",placeholder="Enter the text to get the embeddings")
    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)


# question answering page 
if selected=="GPT":
    st.title("What's on Your Mind?")

    # text box to enter a prompt /
    user_prompt = st.text_area(label="",placeholder="Ask OnlyAI.... ")
    if st.button("Get an Answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)

# Text-to-Speech page
if selected == "Text-to-Speech":
    st.title("🔊 Text-to-Speech")
    input_text = st.text_area(label="Enter text to convert to speech", placeholder="Type something here...")
    language = st.selectbox("Select language", ["en", "es", "fr", "de", "it"])
    
    if st.button("Convert to Speech"):
        if input_text:
            tts_file = text_to_speech(input_text, lang=language)
            if tts_file:
                with open(tts_file, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(label="Download Audio", data=audio_bytes, file_name=tts_file, mime="audio/mp3")
        else:
            st.warning("Please enter some text to convert to speech.")


# Speech-to-Text page
if selected == "Speech-to-Text":
    st.title("🗣️ Speech-to-Text")
    uploaded_audio = st.file_uploader("Upload an audio file ...", type=["mp3", "wav", "m4a"])

    if st.button("Convert to Text"):
        if uploaded_audio:
            # Save the uploaded file to the working directory
            audio_file_path = os.path.join(working_directory, "uploaded_audio.mp3")
            with open(audio_file_path, "wb") as f:
                f.write(uploaded_audio.read())

            try:
                # Perform transcription
                result_text = speech_to_text(audio_file_path)
                st.markdown(f"**Transcription:** {result_text}")
            except Exception as e:
                st.error(f"Error during transcription: {e}")
        else:
            st.warning("Please upload an audio file to convert to text.")