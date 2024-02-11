import json
import requests

from dotenv import load_dotenv
load_dotenv() #loading env variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai 
import re
import base64
from PIL import Image



genai.configure(api_key="API_KEY")

def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt, question])
        return response.text 
    except Exception as e:
        print("Error in generating Gemini response:", e)
        return None

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows: 
        print(row)
    return rows 

def encode_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    encoded = base64.b64encode(image_bytes).decode()
    return encoded

image_paths = [
    "b.jpg",
    "a.jpg",
    "ab.webp"
]

social_media_images = {
    "Twitter": "twitter.png",
    "YouTube": "you.png",
    "Instagram": "ig.png",
    "Facebook": "face.png",
    "hand": "an.gif",
    "logo": "logo.png"

}

    
    

def generate_css_code(image_paths):
    css_code = "<style>\n"
    css_code += "[data-testid='stAppViewContainer'] {\n"
    css_code += "background-size: cover;\n"
    css_code += "animation: cycleBackground 15s linear infinite;\n"
    css_code += "}\n"

    # Generate keyframes for cycling through images
    num_images = len(image_paths)
    step = 100 / num_images
    for i, image_path in enumerate(image_paths):
        encoded_image = encode_image(image_path)
        css_code += f"@keyframes keyframe{i} {{\n"
        css_code += f"0% {{background-image: url('data:image/gif;base64,{encoded_image}');}}\n"
        css_code += f"{step*i}% {{background-image: url('data:image/gif;base64,{encoded_image}');}}\n"
        css_code += f"{step*(i+1)}% {{background-image: url('data:image/gif;base64,{encode_image(image_paths[(i+1)%num_images])}');}}\n"
        css_code += "}\n"

    # Combine keyframes
    css_code += "@keyframes cycleBackground {\n"
    for i in range(num_images):
        css_code += f"{i * step}% {{ background-image: url('data:image/gif;base64,{encode_image(image_paths[i])}'); }}\n"
    css_code += f"{num_images * step}% {{ background-image: url('data:image/gif;base64,{encode_image(image_paths[0])}'); }}\n"
    css_code += "}\n"

    css_code += "</style>"
    return css_code

def display_social_media(social_media_images):
    st.markdown("""
    <style>
        .social-media-icons {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
        }
        .social-media-icons img {
            width: 40px;
            margin: 0 10px;
            transition: transform 0.3s ease-in-out;
        }
        .social-media-icons img:hover {
            transform: scale(1.2);
        }
    </style>
    <div class="social-media-icons">
        <a href="https://www.youtube.com"><img src="twitter.png" alt="Twitter"></a>
        <a href="https://www.youtube.com"><img src="you.png" alt="YouTube"></a>
        <a href="https://www.instagram.com"><img src="ig.png" alt="Instagram"></a>
        <a href="https://www.facebook.com"><img src="face.png" alt="Facebook"></a>
    """, unsafe_allow_html=True)

def display_image_with_base64(image_path):
    encoded_image = encode_image(image_path)
    html_code = f"""
    <style>
        # .image-container {{
        #     position: fixed;
        #     top: -5;
        #     left: -20;
        #     width: 20%;
        #     height: 100vh;
        #     overflow: hidden;
        #     display: flex;
        #     justify-content: center;
        #     align-items: flex-start;
        # }}
        .image-container img {{
            max-height: 100vh;
        }}
    </style>
    <div class="image-container">
        <img src="data:image/png;base64, {encoded_image}" alt="Red dot" />
    </div>

    """
    st.markdown(html_code, unsafe_allow_html=True)

def display_image_02with_base64(image_path2):
    encoded_image2 = encode_image(image_path2)
    html_code = f"""
    <style>
        .image-container {{
            position: fixed;
            top: 0;
            opacity: 50;
            right: 0;
            max-width: 13%; /* Adjust the size as needed */
            overflow: hidden;
            z-index: 9999; /* Ensure it's on top */
        }}
        .image-container img {{
            width: 100%;
            height: auto;
        }}
    </style>
    <div class="image-container">
        <img src="data:image/png;base64, {encoded_image2}" alt="Image" />
    </div>

    """
    st.markdown(html_code, unsafe_allow_html=True)

# def display_image_with_base64(image_path):
#     encoded_image = encode_image(image_path)
#     html_code = f"""
#     <div>
#         <img src="data:image/png;base64, {encoded_image}" alt="Red dot" />
#     </div>
#     """
#     st.markdown(html_code, unsafe_allow_html=True)


prompt= """
    You are an expert in converting English questions to SQL query and in medical diagnoses!
    The SQL database has the name PATIENT and has the following columns - NAME, AGE, 
    ILLNESS, BMI, ERSTATUS\n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM PATIENT ;
    \nExample 2 - Tell me all the patients who had ERSTATUS?, 
    the SQL command will be something like this SELECT * FROM PATIENT 
    where ERSTATUS="Positive"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """

formatting_prompt = """
                    You are an expert in formatting SQL data output. You will take a question and
                    SQL output, and you will generate a bulleted list of outputs formatted in plain text 
                    without parantheses.\n\nFor example,\n Example 1 - "edgar, alexandria, hans", 
                    The output should be: The names of patients who had ERSTATUS are: \n
                    \t - Edgar \n
                    \t - Alexandria \n
                    \t - Hans \n 
                    Please let me know how else I can assist you in understanding your patient histories.
   """



st.set_page_config(page_title="MedMasters SQL Query Tool")

st.header("MedMasters SQL Query Tool")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"patient.db")
    for row in response:
        string = str(row)[1:-1]
      

        st.header(string.strip(",").strip("'"))


image_path = "c.gif"

encoded_image = encode_image(image_path)

css_code = f"""
<style>


[data-testid="stAppViewContainer"] {{
    background-image: url('data:image/gif;base64,{encoded_image}');
    background-size: cover;

}}
</style>

"""

st.markdown(css_code, unsafe_allow_html=True)
css_code = generate_css_code(image_paths)

# Apply CSS to the Streamlit app
st.markdown(css_code, unsafe_allow_html=True)

display_social_media(social_media_images)

image_path = "path_to_your_image.png"



#display_image_with_base64("C:/Users/hayim/Documents/Github/Hacklytics/twitter.png")
#display_image_with_base64("an.gif")
display_image_02with_base64("logo.png")