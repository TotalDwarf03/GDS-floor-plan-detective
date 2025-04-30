from pydantic import BaseModel, Field
import json

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

# Random status messages for toasts
STATUS_MESSAGES = {
    "passing": [
        "🔍 Case closed! This floor plan is perfect!",
        "🕵️‍♂️ Elementary, my dear Watson! All elements present!",
        "🔎 Investigation complete - this floor plan is spotless!",
        "📋 All evidence accounted for - perfect floor plan!",
        "🔦 Nothing to see here, everything's in order!",
        "📝 Case file complete - all requirements met!",
        "🔍 Mystery solved - this floor plan is flawless!",
        "🕵️‍♂️ The evidence is clear - perfect execution!",
        "🔎 All clues point to a perfect floor plan!",
        "📋 Case closed with flying colors!"
    ],
    "failing": [
        "🔍 Missing evidence detected!",
        "🕵️‍♂️ Elementary, my dear Watson - some elements are missing!",
        "🔎 Investigation reveals missing pieces!",
        "📋 Case file incomplete - more details needed!",
        "🔦 Found some gaps in the evidence!",
        "📝 Need more clues to solve this case!",
        "🔍 Mystery remains - some elements are missing!",
        "🕵️‍♂️ The evidence suggests more work needed!",
        "🔎 Some clues are still missing!",
        "📋 Case remains open - more details required!"
    ]
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