# Floor Plan Detective 🕵️‍♂️

A Streamlit application that analyzes floor plans in PDF format to check for required elements, providing a fun and engaging detective-themed interface.

## Contents

- [Floor Plan Detective 🕵️‍♂️](#floor-plan-detective-️️)
  - [Contents](#contents)
  - [Disclaimer](#disclaimer)
  - [Features](#features)
  - [Video Demo](#video-demo)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)


## Disclaimer

This project was created during the GDS Hackathon in Leeds (We hacked planning). It contains a majority of AI generated code, and is not intended to be used as a production application. The tool was developed between the 30th of April and the 1st of May 2025.

The scope of the project was to create a tool to show how AI could be used to help replace some of the manual, time-consuming tasks that are part of the planning process. This would help councils to process planning applications more quickly and efficiently, freeing up resources to focus on more complex cases.

This tool focuses on validating design diagrams, submitted with applications for householder planning permission. Currently, there are no tools in place that verify diagrams, so this is a step towards automating this process.

## Features

- PDF upload and preview
- AI-powered floor plan analysis
- Detective-themed feedback and messages
- Text-to-speech notifications
- Visual feedback with emojis and balloons
- Real-time analysis results

## Video Demo

A demonstration of the tool can be found within the repository: [video_demo.mov](./demo/video_demo.mov)

![Floor Plan Detective Demo](https://github.com/TotalDwarf03/GDS-floor-plan-detective/blob/main/demo/readme_demo.gif)

## Requirements

- Python 3.8+
- Streamlit
- Azure OpenAI API access
- Poetry Package Manager

## Installation

1. Clone the repository

2. Change into the root of the repository:
```bash
cd gds-leeds-hack-25
```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
poetry install
```

5. Create a `.env` file with your Azure OpenAI credentials:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_MODEL=gpt-4.1-mini
OPENAI_API_VERSION=2025-03-01-preview 
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Upload a PDF containing floor plans (Examples are available in [`example_floorplans/`](./example_floorplans/))
3. Click "Investigate Floor Plan" to start the analysis
4. View the results and feedback

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 