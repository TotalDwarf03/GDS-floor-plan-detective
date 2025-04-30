# Floor Plan Detective 🕵️‍♂️

A Streamlit application that analyzes floor plans in PDF format to check for required elements, providing a fun and engaging detective-themed interface.

## Features

- PDF upload and preview
- AI-powered floor plan analysis
- Detective-themed feedback and messages
- Text-to-speech notifications
- Visual feedback with emojis and balloons
- Real-time analysis results

## Requirements

- Python 3.8+
- Streamlit
- Azure OpenAI API access
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

1. Create a `.env` file with your Azure OpenAI credentials:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_MODEL=gpt-4.1-mini
OPENAI_API_VERSION=2025-03-01-preview 
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Upload a PDF containing floor plans
3. Click "Investigate Floor Plan" to start the analysis
4. View the results and feedback

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 