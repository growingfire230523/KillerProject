import streamlit as st
import json
import os
from streamlit_option_menu import option_menu
# import whisper
from PIL import Image
from gemini_utility import (load_gemini_pro_model,gemini_pro_vision_response,embedding_model_response,gemini_pro_response,text_to_speech,speech_to_text)
# import speech_recognition as sr
# import tempfile
# from pydub import AudioSegment
import replicate as rp
import requests
import re

# accessing the working_directory 
working_directory = os.path.dirname(os.path.abspath(__file__))
# print(working_directory)
import openai
# import urllib.request 

# configuring openai api key --
# config_data = json.load(open(f"{working_directory}/config.json"))
# OPEN_AI_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = "sk-proj-51gXGw28EmoS5hwKltRbT3BlbkFJYUvYKcJ7fr2ahp4eHBPK"
# setting up the page configuration 
st.set_page_config(
    page_title = "OnlyAI",
    page_icon = "🧠",
    layout = "centered"
)

class NSFWError(Exception):
    """Exception raised for NSFW content detection."""
    pass

# logo_url = "owner.jpg"
# st.image(logo_url,width=51)
# st.video()
# video_file = open('We.mp4', 'rb')
# video_bytes = video_file.read()
# st.video(video_bytes)
# st.video("We.mp4", format="video/mp4", start_time=0,*, subtitles=None, end_time=None, loop=True, autoplay=True, muted=True)

with st.sidebar:

    selected = option_menu(menu_title="We're OnlyAI!",options=["GPT","Image Generation","Image Captioning","Text-to-Speech","ChatBot","Embed text","About Me"],menu_icon= 'robot',icons=['question-diamond','file-image-fill','card-image','mic-fill','chat-dots-fill','card-text','person-workspace'],default_index=0)


# (removed functionalities : {"Image Generation",'file-image-fill'},{"Speech-to-Text",'mic',} )
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
# if selected=="Image Generation" :
#     # streamlit page title 
#     st.title("⏳ Image Generator ")
#     # text input for image generation prompt 
#     img_description = st.text_input('Image Description')

#     if st.button("Generate Image"):
#         generated_image = generate_image(img_description)
#         st.image(generated_image)

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
    language = st.selectbox("Select language", ["en","hi", "es", "fr", "de", "it"])
    
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


# # Speech-to-Text page
if selected == "Speech-to-Text":
    st.title("🗣️ Speech-to-Text")
    uploaded_audio = st.file_uploader("Upload an audio file ...", type=["mp3", "wav", "m4a"])

    if st.button("Convert to Text"):
        if uploaded_audio:
            audio_file_path = os.path.join(os.getcwd(), "uploaded_audio.mp3")
            with open(audio_file_path, "wb") as f:
                f.write(uploaded_audio.read())

            try:
                result_text = speech_to_text(audio_file_path)
                st.markdown(f"**Transcription:** {result_text}")
            except Exception as e:
                st.error(f"Error during transcription: {e}")
        else:
            st.warning("Please upload an audio file to convert to text.")


# image generation page 
if selected=="Image Generation":

    if not hasattr(st, "global_image_generated_counter"):
        st.global_image_generated_counter = 0

    if "user_API_key" in st.session_state:
        st.session_state.user_API_key = None

    with st.form("model_selection_form"):
        st.markdown("<h4 style='text-align: center'>Choose a model from the dropdown to begin</h4>", unsafe_allow_html=True)
        # option = st.selectbox("**Select the model you want to use**", (None, "Stable Diffusion", "Anything-v4.0", "Waifu Diffusion", "Vintedios Diffusion"), index=1)
        option = st.selectbox("**Select the model you want to use**", (None, "Stable Diffusion"), index=0)
        model_select_button = st.form_submit_button("Select Model")
        
        # if model_select_button:
        #     with st.spinner("Setting Model."):
        #         st.write(f"Model '{option}' selected.")
        #     st.toast(f"Model '{option}' has been selected.")



    if option is not None:
        st.sidebar.markdown("<h2 style='text-align: center;'>Enter the API key</h2>", unsafe_allow_html=True)
        api_key_option = st.sidebar.radio("Select the API key option", ["Use your Own API key"])
        # api_key_option = st.sidebar.radio(["Use your Replicate API-key"])
        
        if api_key_option == "Community API key":
            with st.expander("Community Credits Progress Bar", expanded=True):
                st.write("Feel free to generate images with the 'IMAGINATE HUB' community credits (check the limit below) or use your own Replicate API key in the sidebar by selecting 'Use your own API key'.")
                st.progress(st.global_image_generated_counter, f"'IMAGINATE HUB' community can generate {200-st.global_image_generated_counter} more images")
                
        else: 
            st.session_state.user_API_key = st.sidebar.text_input(label="Enter your replicate API key:", type="password")
            if st.session_state.user_API_key is not None: 
                if not re.match("^r8_", st.session_state.user_API_key) or not len(st.session_state.user_API_key) > 30:
                    st.sidebar.error("Please enter a correct API key. Please check the below link to learn how to get a replicate API key.")   
            st.sidebar.markdown("<h4><a href='https://drive.google.com/file/d/1uTBewM6toJZ_wU1i-xSHl2TN5i-hSA55/view?usp=sharing'>How to get replicate API key?</a></h4>", unsafe_allow_html=True)
        
        # st.session_state.user_API_key = st.sidebar.text_input(label="Enter your replicate API key:", type="password")
        # if st.session_state.user_API_key is not None: 
        #     if not re.match("^r8_", st.session_state.user_API_key) or not len(st.session_state.user_API_key) > 30:
        #         st.sidebar.error("Please enter a correct API key. Please check the below link to learn how to get a replicate API key.")   
        # st.sidebar.markdown("<h4><a href='https://drive.google.com/file/d/1SU1dc5Gx1N2g4X7OkOhI2OPMFupHat4g/view?usp=sharing'>How to get replicate API key?</a></h4>", unsafe_allow_html=True)
        

        # with st.sidebar:
        # if option == "Stable Diffusion":
            # with st.form("stable_diffusion_parameter_form"):
            #     st.write("Control Stable Diffusion Model Parameters Here")
                # sd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
            sd_num_inference_steps = 50
            # sd_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL"], index=0)
            sd_scheduler_options = "DPMSolverMultistep"
            # sd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
            sd_seed = 0
                    # sd_submit_form = st.form_submit_button("Apply") 
                    # if sd_submit_form:
                    #     st.success("Applied!")
                    #     if not re.match("^[0-9]+$", sd_seed):
                    #         st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                            
        #     elif option == "Anything-v4.0":
        #         with st.form("anything_v4_parameter_form"):
        #             st.write("Control Anything-v4.0 Model Parameters Here")
        #             at_num_outputs = st.radio("Choose no of images you like to generate", ["1", "4"], index=0)
        #             at_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=20, value=20, step=5)
        #             at_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL", "PNDM", "KLMS"], index=0)
        #             at_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
        #             at_submit_form = st.form_submit_button("Apply")
        #             if at_submit_form:
        #                 st.success("Applied!")
        #                 if not re.match("^[0-9]+$", at_seed):
        #                     st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                            
        #     elif option == "Waifu Diffusion":
        #         with st.form("waifu_diffusion_parameter_form"):
        #             st.write("Control Waifu Diffusion Model Parameters Here")
        #             wd_num_outputs = st.radio("Choose no of images you like to generate", ["1", "4"], index=0)
        #             wd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
        #             wd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
        #             wd_submit_form = st.form_submit_button("Apply")
        #             if wd_submit_form:
        #                 st.success("Applied!")
        #                 if not re.match("^[0-9]+$", wd_seed):
        #                     st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
                            
        #     else:
        #         with st.form("vintedios_diffusion_parameter_form"):
        #             st.write("Control Vintedios Diffusion Model Parameters Here")
        #             vd_num_inference_steps = st.slider("Adjust the slider for no of denoising steps.", min_value=5, max_value=50, value=50, step=10)
        #             vd_scheduler_options = st.selectbox("Choose a scheduler.", ["DPMSolverMultistep", "DDIM", "K_EULER", "K_EULER_ANCESTRAL", "PNDM", "KLMS"], index=0)
        #             vd_seed = st.text_input("Enter a seed (optional) (Leave this 0 for random seed)", 0)
        #             vd_submit_form = st.form_submit_button("Apply")
        #             if vd_submit_form:
        #                 st.success("Applied!")
        #                 if not re.match("^[0-9]+$", vd_seed):
        #                     st.error("Please enter a seed number not a String in a 'Enter a seed' field above.")
            
        #     st.markdown("<h4 style='color: yellow'>More parameter controls coming soon 🔜.</h4>", unsafe_allow_html=True)
                

    #         st.markdown(
    #     """ -----
    #     [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MonishSoundarRaj/image-generator-streamlit)
    #     [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=blue")](https://www.linkedin.com/in/monish-soundar-raj-613207218/)
    #     """,
    #     unsafe_allow_html=True
    # )
    #         st.markdown("-----")
    #         st.markdown("<div style='background: #FFFDD0'><a style = 'text-decoration: none' href='https://forms.gle/YiUezL6x1tT7ui6z9'><p style='padding:10px; color: red; font-size: 16px; text-align: center; font-style: bold'>Feedback or specific model request form. ➡️</p></a></div>", unsafe_allow_html=True)
            
        with st.form("Enter_Prompt_form"):
            prompt = st.text_area("Enter Image Generation Prompt")
            prompt_submit = st.form_submit_button("Submit Prompt")
            
        if api_key_option != "Community API key":
            os.environ["REPLICATE_API_TOKEN"] = st.session_state.user_API_key
        
        placeholder = st.empty()
        
        placeholder.markdown("<div style='margin: 20px;'><h3 style='text-align: center; padding: 50px'>Image will be displayed here once generated.</h3></div>", unsafe_allow_html=True)
        
        if prompt_submit:
            placeholder.empty()
            model_selected = None
            if option == "Stable Diffusion":
                model_selected = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"
                input={"prompt": prompt,"num_inference_steps":sd_num_inference_steps, "scheduler":sd_scheduler_options, **({"seed": int(sd_seed)} if int(sd_seed) > 0 else {})}
            # elif option == "Anything-v4.0":
            #     model_selected = "cjwbw/anything-v4.0:42a996d39a96aedc57b2e0aa8105dea39c9c89d9d266caf6bb4327a1c191b061"
            #     input={"prompt": prompt, "num_outputs":int(at_num_outputs), "num_inference_steps":at_num_inference_steps, "scheduler":at_scheduler_options, **({"seed": int(at_seed)} if int(at_seed) > 0 else {})}
            # elif option == "Waifu Diffusion":
            #     model_selected = "cjwbw/waifu-diffusion:25d2f75ecda0c0bed34c806b7b70319a53a1bccad3ade1a7496524f013f48983"
            #     input={"prompt": prompt, "num_outputs":int(wd_num_outputs), "num_inference_steps":wd_num_inference_steps, **({"seed": int(wd_seed)} if int(wd_seed) > 0 else {})}
            # else:
            #     model_selected = "22-hours/vintedois-diffusion:28cea91bdfced0e2dc7fda466cc0a46501c0edc84905b2120ea02e0707b967fd"
                # input={"prompt": prompt, "num_inference_steps":vd_num_inference_steps, "scheduler":vd_scheduler_options, **({"seed": int(vd_seed)} if int(vd_seed) > 0 else {})}
                
            if api_key_option != "Community API key" and st.session_state.user_API_key == None:
                st.error("Enter your API key in the sidebar or select 'Community API key' option.")
            else:
                st.toast("Your prompt has been submitted successfully.")
                with st.spinner("We are working on your image, please do not change or resubmit anything now."):   
                    try:
                        output = rp.run(
                            model_selected,
                            input = input,
                        )
                    except NSFWError as error:
                        st.error("Please enter NSFW prompt, if you think you have entered a NSFW prompt and please reclick on 'Submit Prompt'")
                    
                    if option == "Stable Diffusion" or option == "Vintedios Diffusion":
                        st.success("If you like the generated image download it from the link before changing the parameters.")
                        st.image(output)
                        st.success(f"You can download the image by going here: {output[0]}")
                    else:
                        st.success("If you like the generated image download it from the link before changing the parameters.")
                        if len(output) > 1:
                            for idx, item in enumerate(output):
                                col1, col2 = st.columns(2)
                                col_logic = col1 if idx%2 == 0 else col2
                                with col_logic:
                                    st.image(item)
                            print(output)
                        else:
                            st.image(output)
                        st.success(f"You can download the image by going here: {output}") 
                    
                    if api_key_option == "Community API key":
                        st.global_image_generated_counter += 1
                    
    else:
        pass

    with st.expander("Sample Images Generated with OnlyAI Diffusion Model", expanded=True):
            spacer1, col1, spacer2, col2 = st.columns([0.5,4,0.5,4])
            with open('./prompts/prompts.md', 'r') as file:
                for idx, prompt_line in enumerate(file):
                    model_part, prompt_part = prompt_line.split("Prompt:", 1)
                    col_logic = col1 if idx%2 == 0 else col2
                    with col_logic:
                        st.image(f"./generated_images/out-0 ({idx}).png", width=250, caption=prompt_part.strip() + "\n" + model_part.strip())   


