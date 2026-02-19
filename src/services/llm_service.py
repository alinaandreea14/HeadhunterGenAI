# ==============================================================================
# SETUP & SECURITITY
# ==============================================================================

import streamlit as st
import os
import instructor
from groq import Groq
from dotenv import load_dotenv
from src.models import JobAnalysis

st.set_page_config(page_title="GenAI Headhunter", page_icon="🕵️", layout="wide")

# Load the variables from the .env file
load_dotenv()

# We are trying to get the key from the OS (local) or from Streamlit Secrets (cloud)
api_key = os.getenv("GROQ_API_KEY")

# Fallback for Streamlit Cloud deployment
if not api_key and "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]

# Critical validation: If we don't have a key, we stop the application here.
if not api_key:
    st.error("⛔ CRITICAL ERROR: Missing `GROQ_API_KEY`.")
    st.info("Please create a `.env` file in your project folder and add: GROQ_API_KEY=your_key_here")
    st.stop()

# Configurare Client Groq Global (to avoid constantly resetting it)
client = instructor.from_groq(Groq(api_key=api_key), mode=instructor.Mode.TOOLS)

# ==============================================================================
# AI SERVICE LAYER (LLM logic)
# ==============================================================================

def analyze_job_with_ai(text: str) -> JobAnalysis:
    """
    Sends the cleaned text to Groq and returns the structured object.
    """
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=JobAnalysis,
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an IT Expert Recruiter. Analyze the job text objectively."
                    "Identify technologies and potential problems (red flags)."
                    "Answer strictly in the required format."
                )
            },
            {
                "role": "user", 
                "content": f"Analyze this job description:\n\n{text}"
            }
        ],
        temperature=0.1,
    )