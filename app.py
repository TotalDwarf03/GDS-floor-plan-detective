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
    dimensions: bool = Field(description="Are room dimensions clearly labeled?")
    title_block: bool = Field(description="Is there a title block with project information?")
    legend: bool = Field(description="Is there a legend explaining symbols?")
    room_labels: bool = Field(description="Are all rooms clearly labeled?")
    door_swings: bool = Field(description="Are door swings indicated?")
    window_symbols: bool = Field(description="Are windows clearly marked?")
    furniture: bool = Field(description="Is furniture layout shown?")
    annotations: bool = Field(description="Are there any important annotations?")

st.set_page_config(page_title="Planning Application Floor Plan Analysis", layout="wide")

st.title("Planning Application Floor Plan Analysis")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("PDF Upload and Preview")
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
                            "text": "Analyze this floor plan and check for the following elements: scale bar, compass/north reference, room dimensions, title block, legend, room labels, door swings, window symbols, furniture layout, and annotations."
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
                                        "text": "Analyze this floor plan and check for the following elements: scale bar, compass/north reference, room dimensions, title block, legend, room labels, door swings, window symbols, furniture layout, and annotations."
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
                    
                    # Store the results in session state
                    st.session_state.checklist_results = parsed_data
                    
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(tmp_file_path)

with col2:
    st.header("Floor Plan Checklist")
    
    # Initialize checklist results in session state if not exists
    if 'checklist_results' not in st.session_state:
        st.session_state.checklist_results = {
            "scale_bar": False,
            "compass": False,
            "dimensions": False,
            "title_block": False,
            "legend": False,
            "room_labels": False,
            "door_swings": False,
            "window_symbols": False,
            "furniture": False,
            "annotations": False
        }
    
    # Display checklist items
    st.write("### Required Elements")
    st.write("Scale Bar:", "✅ Present" if st.session_state.checklist_results["scale_bar"] else "❌ Missing")
    st.write("Compass/North Reference:", "✅ Present" if st.session_state.checklist_results["compass"] else "❌ Missing")
    st.write("Room Dimensions:", "✅ Present" if st.session_state.checklist_results["dimensions"] else "❌ Missing")
    st.write("Title Block:", "✅ Present" if st.session_state.checklist_results["title_block"] else "❌ Missing")
    
    st.write("### Additional Elements")
    st.write("📋 Legend:", "✅ Present" if st.session_state.checklist_results["legend"] else "❌ Missing")
    st.write("🏠 Room Labels:", "✅ Present" if st.session_state.checklist_results["room_labels"] else "❌ Missing")
    st.write("🚪 Door Swings:", "✅ Present" if st.session_state.checklist_results["door_swings"] else "❌ Missing")
    st.write("🪟 Window Symbols:", "✅ Present" if st.session_state.checklist_results["window_symbols"] else "❌ Missing")
    st.write("🪑 Furniture Layout:", "✅ Present" if st.session_state.checklist_results["furniture"] else "❌ Missing")
    st.write("📝 Annotations:", "✅ Present" if st.session_state.checklist_results["annotations"] else "❌ Missing") 