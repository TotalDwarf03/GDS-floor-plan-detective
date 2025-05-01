from pydantic import BaseModel, Field
import json

# Define emojis for each check
CHECK_EMOJIS = {
    "scale_bar": "📏",
    "compass": "🧭",
    "address": "📍",
    "room_labels": "🏠",
}

class DiagramExtraction(BaseModel):
    scale_bar: bool = Field(description="Does the image have a scale bar?")
    compass: bool = Field(description="Does the image have a compass/north reference?")
    room_labels: bool = Field(description="Are all rooms clearly labeled?")
    address: bool = Field(description="Is the address clearly labeled?")


# TODO: Support for non yes no stuff
# Plan Type: Existing, Proposed, Both
# Scale: 1:100, 1:200, 1:500, 1:1000
# Floor Space (Grace internal Area)

# Random status messages for toasts
STATUS_MESSAGES = {
    "passing": [
        "Case closed! This floor plan is perfect! 🔍",
        "Elementary, my dear Watson! All elements present! 🕵️‍♂️",
        "Investigation complete - this floor plan is spotless! 🔎",
        "All evidence accounted for - perfect floor plan! 📋",
        "Nothing to see here, everything's in order! 🔦",
        "Case file complete - all requirements met! 📝",
        "Mystery solved - this floor plan is flawless! 🔍",
        "The evidence is clear - perfect execution! 🕵️‍♂️",
        "All clues point to a perfect floor plan! 🔎",
        "Case closed with flying colors! 📋"
    ],
    "failing": [
        "Missing evidence detected! 🔍",
        "Elementary, my dear Watson - some elements are missing! 🕵️‍♂️",
        "Investigation reveals missing pieces! 🔎",
        "Case file incomplete - more details needed! 📋",
        "Found some gaps in the evidence! 🔦",
        "Need more clues to solve this case! 📝",
        "Mystery remains - some elements are missing! 🔍",
        "The evidence suggests more work needed! 🕵️‍♂️",
        "Some clues are still missing! 🔎",
        "Case remains open - more details required! 📋"
    ]
}