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

# Load checklist configuration
with open('checklist_config.json', 'r') as f:
    checklist_config = json.load(f)

# Create Pydantic model dynamically from checklist config
class DiagramExtraction(BaseModel):
    scale_bar: bool = Field(description=checklist_config["floorplan_checks"]["scale_bar"]["description"])
    compass: bool = Field(description=checklist_config["floorplan_checks"]["compass"]["description"])
    dimensions: bool = Field(description=checklist_config["floorplan_checks"]["dimensions"]["description"])
    title_block: bool = Field(description=checklist_config["floorplan_checks"]["title_block"]["description"])
    legend: bool = Field(description=checklist_config["floorplan_checks"]["legend"]["description"])
    room_labels: bool = Field(description=checklist_config["floorplan_checks"]["room_labels"]["description"])
    door_swings: bool = Field(description=checklist_config["floorplan_checks"]["door_swings"]["description"])
    window_symbols: bool = Field(description=checklist_config["floorplan_checks"]["window_symbols"]["description"])
    furniture: bool = Field(description=checklist_config["floorplan_checks"]["furniture"]["description"])
    annotations: bool = Field(description=checklist_config["floorplan_checks"]["annotations"]["description"])

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
            key: False for key in checklist_config["floorplan_checks"].keys()
        }
    
    if uploaded_file is not None:
        if st.button("Analyze Floor Plan"):
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
                        "text": "Analyze this floor plan and check for the following elements: " + 
                               ", ".join([item["description"] for item in checklist_config["floorplan_checks"].values()])
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
                                    "text": "Analyze this floor plan and check for the following elements: " + 
                                           ", ".join([item["description"] for item in checklist_config["floorplan_checks"].values()])
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
                st.session_state.analysis_complete = True
        
        # Only show checklist if analysis is complete
        if st.session_state.get('analysis_complete', False):
            # Calculate overall score
            total_checks = len(st.session_state.checklist_results)
            passed_checks = sum(1 for value in st.session_state.checklist_results.values() if value)
            percentage = (passed_checks / total_checks) * 100
            
            # Display overall score
            st.write("### Overall Score")
            st.write(f"Passed: {passed_checks}/{total_checks} checks")
            
            if percentage == 100:
                st.write(f"Percentage: {percentage:.0f}% ✅")
            else:
                st.write(f"Percentage: <span style='color:red'>{percentage:.0f}% ❌</span>", unsafe_allow_html=True)
                st.error("⚠️ The floor plan should be rejected due to missing required elements.")
            
            # Display checklist items
            st.write("### Floor Plan Requirements")
            
            # Get failed and passed checks
            failed_checks = {k: v for k, v in checklist_config["floorplan_checks"].items() 
                           if not st.session_state.checklist_results[k]}
            passed_checks = {k: v for k, v in checklist_config["floorplan_checks"].items() 
                           if st.session_state.checklist_results[k]}
            
            # Display failed checks first
            if failed_checks:
                st.write("#### Missing Requirements")
                for key, config in failed_checks.items():
                    st.write(f"{config['emoji']} {config['name']}:", 
                            "<span style='color:red'><b>❌ Missing</b></span>", 
                            unsafe_allow_html=True)
            
            # Display passed checks
            if passed_checks:
                st.write("#### Present Requirements")
                for key, config in passed_checks.items():
                    st.write(f"{config['emoji']} {config['name']}:", 
                            "✅ Present", 
                            unsafe_allow_html=True) 