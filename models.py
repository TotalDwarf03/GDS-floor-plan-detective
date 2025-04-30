from pydantic import BaseModel, Field
import json

# Load checklist configuration
with open('checklist_config.json', 'r') as f:
    checklist_config = json.load(f)

# Define emojis for each check
CHECK_EMOJIS = {
    "scale_bar": "📏",
    "compass": "🧭",
    "dimensions": "📐",
    "title_block": "📋",
    "legend": "📋",
    "room_labels": "🏠",
    "door_swings": "🚪",
    "window_symbols": "🪟",
    "furniture": "🪑",
    "annotations": "📝"
}

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