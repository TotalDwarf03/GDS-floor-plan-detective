import streamlit as st
import pdf2image
import tempfile
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import base64
from PIL import Image
import io
from pydantic import BaseModel, Field
import json

# Load environment variables
load_dotenv()

# Configure Azure OpenAI
openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
api_version = os.environ.get("OPENAI_API_VERSION", "2024-12-01-preview")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

class DiagramExtraction(BaseModel):
    scale_bar: bool = Field(description="Does the image have a scale bar?")
    compass: bool = Field(description="Does the image have a compass/north reference?")

st.set_page_config(page_title="PDF Preview and Analysis", layout="wide")

st.title("PDF Upload, Preview, and Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(tmp_file_path)
        
        # Display each page
        for i, image in enumerate(images):
            st.image(image, caption=f'Page {i+1}', use_container_width=True)
        
        # Add a section for AI analysis
        st.header("AI Analysis")
        
        if st.button("Analyze PDF"):
            with st.spinner("Analyzing document..."):
                # Convert images to base64
                image_messages = []
                for i, image in enumerate(images):
                    # Convert PIL image to bytes
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Encode as base64
                    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
                    
                    image_messages.append({
                        "type": "input_image",
                        "image": img_base64
                    })
                
                # Prepare the message content
                message_content = [
                    {
                        "type": "input_text",
                        "text": "Does the image have a scale bar and compass/north reference?"
                    }
                ]
                message_content.extend(image_messages)
                
                completion = client.responses.parse(
                    model=openai_model,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": "Does the image have a scale bar and compass/north reference?"
                                },
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/jpeg;base64,{image_messages[0]['image']}"
                                }
                            ]
                        }
                    ],
                    text_format=DiagramExtraction
                )

                # Extract the parsed response
                output_text = completion.output[0].content[0].text
                parsed_data = json.loads(output_text)
                
                # Display the results
                st.write("Scale Bar:", "✅ Yes" if parsed_data["scale_bar"] else "❌ No")
                st.write("Compass:", "✅ Yes" if parsed_data["compass"] else "❌ No")
            
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path) 