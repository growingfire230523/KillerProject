import os 
import json 
import openai
import whisper
from gtts import gTTS
from PIL import Image
# importing image processing lib //
import google.generativeai as genai
import urllib.request 
# import speech_recognition as sr
# import tempfile



# accessing the working_directory 
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"
# print(config_file_path)
config_data = json.load(open(config_file_path))

# loading the api key //s
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
openai.api_key = "sk-proj-51gXGw28EmoS5hwKltRbT3BlbkFJYUvYKcJ7fr2ahp4eHBPK"
# configuring google.generativeai with api key
genai.configure(api_key=GOOGLE_API_KEY)

# function for image generation using OPENAI key 
# def generate_image(image_description):
#     img_response = openai.Image.create(
#         prompt = image_description,
#         n=1,
#         size = "512x512"
#     )
    
#     img_url = img_response['data'][0]['url']
#     urllib.request.urlretrieve(img_url,'img.png')
#     img = Image.open("img.png")
#     return img

# function to load model gemini-pro-model for chatbot
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# function for image captioning //
def gemini_pro_vision_response(prompt,image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-pro-vision")
    response = gemini_pro_vision_model.generate_content([prompt,image])
    result = response.text
    return result

# testing here only over an image from gallery 
# image = Image.open("cat2.jpg")
# prompt = "What is inside this jpg image"
# output = gemini_pro_vision_response(prompt,image)
# print(output)

# function to get embeddings for text 
def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,content=input_text,task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list 

# output = embedding_model_response("Who is Andrew Tate")
# print(output)

# function to get a response from gemini-pro LLM
def gemini_pro_response(user_prompt) :
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result

# output = gemini_pro_response("What is LLM ?")
# print(output)

# function to convert text to speech and save as mp3 file :
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts_file = "output.mp3"
    tts.save(tts_file)
    return tts_file


# Function for speech-to-text
# def speech_to_text(audio_file_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file_path)
#     return result["text"]

