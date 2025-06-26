from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set the Google Generative AI API key
api_key = os.getenv("GOOGLE_AI_API_KEY")
genai.configure(api_key = api_key)

## Function to load the Gemini 2.5 Flash model

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(user_input, image_parts, prompt):
    response = model.generate_content([
        {"text": prompt},         # System-level or guiding prompt
        {"text": user_input},     # User's question or task
        *image_parts              # Image(s) as input
    ])
    return response.text


## Function to handle the image


def handle_images(uploaded_images):
    image_parts = []
    for uploaded_image in uploaded_images:
        bytes_data = uploaded_image.getvalue()
        image_parts.append({
            "mime_type": uploaded_image.type,
            "data": bytes_data
        })
    return image_parts


# Streamlit app configuration

st.set_page_config(
    page_title="Multi Language Invoice Extractor",
    page_icon="🤖",
    layout="wide",
)

st.markdown("<h1 style='text-align: center;'>Gemini Application</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Gemini 1.5 Flash</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>This demo showcases the capabilities of the Gemini 1.5 Flash model by Google Generative AI. You can input text, upload an image, and provide a prompt to generate a response.</p>", unsafe_allow_html=True)



# Image upload
uploaded_files = st.file_uploader("Upload an image of an invoice: ", type=["jpg", "jpeg", "png"], key = "image", accept_multiple_files=True)

image = ""

if uploaded_files:
    cols = st.columns(len(uploaded_files)) # Create columns for each uploaded image
    for idx, img_file in enumerate(uploaded_files):
        img = Image.open(img_file)
        with cols[idx]:
            st.image(img, caption=img_file.name, use_container_width=True)
    st.write(f"{len(uploaded_files)} image(s) uploaded successfully!")
else:
    st.write("No image uploaded.")

# Input text box

input_text = st.text_input("Input Prompt: ", key = "input_text")
submit_button = st.button("Tell me about this invoice", key = "submit_button")

input_prompt = """
You are a helpful assistant and expert in understanding invoices. An image will be uploaded as an invoice.
You have to analyze the invoice and provide a detailed description of its contents.
Also, you have to answer any questions related to the invoice based on the image provided.
"""

## If submit button is clicked, generate the response

if submit_button:
    if not uploaded_files and not input_text:
        st.error("❌ No image uploaded. Please upload an image of an invoice and/or provide a text input.")
        st.stop()

    image_parts = handle_images(uploaded_files)

    with st.spinner("⏳ Generating response..."):
        if input_text:
            response = get_gemini_response(input_text, image_parts, input_prompt)
        else:
            response = get_gemini_response(input_prompt, image_parts, input_prompt)

        if response:
            st.success("✅ Response generated successfully!")
            st.subheader("Response:")
            st.write(response)
        else:
            st.error("⚠️ Failed to generate a response. Please try again.")