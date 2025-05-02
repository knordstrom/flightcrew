#!/usr/bin/env python
import os
import sys
import warnings

from datetime import datetime

from dotenv import load_dotenv

from flightcrew.crew import FlightCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_inquiry_file():
    """
    Load the contents of the file at ../../knowledge/inquiry into a string variable.
    """
    file_path: str = os.path.join(os.path.dirname(__file__), '../../knowledge/inquiry')
    try:
        print(__file__)
        with open(file_path, 'r') as file:
            inquiry_content = file.read()
        return inquiry_content
    except FileNotFoundError:
        raise Exception(f"No inquiry found at {file_path}.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the inquiry file: {e}")

def run():
    """
    Run the crew.
    """
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),'../../.env'), override=True)
    inputs = {
        'topic': 'Find flights to SAF after June 1st, 2025',
        'start_date': '2025-06-01', # str(datetime.now().date()),
        'current_year': str(datetime.now().year)
    }

    inquiry_content: str = load_inquiry_file()

    try:
        FlightCrew(goal=f'{inquiry_content}. Then use the response to publish a report on the subject in markdown').crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
