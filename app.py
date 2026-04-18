import streamlit as st
import PyPDF2
import json
import os
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- 1. UI CONFIGURATION ---
st.set_page_config(page_title="AI Project Assistant", page_icon="🤖", layout="wide")

st.title("🤖 AI BA Assistant")
st.markdown("""
    This tool automates the **Document-to-Task** workflow. 
    It reads your project docs, summarizes context, and breaks down actionable tasks for your team.
""")

# --- 2. INITIALIZE AI CLIENT ---
# Initialize OpenAI client from the environment or Streamlit secrets.
# Recommended: set the OPENAI_API_KEY environment variable, or add it to
# .streamlit/secrets.toml as OPENAI_API_KEY = "sk-..."
api_key = os.getenv("OPENAI_API_KEY")
if not api_key and isinstance(st.secrets, dict) and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

if not api_key:
    st.sidebar.error(
        "OpenAI API key not found. Set OPENAI_API_KEY env var or add to .streamlit/secrets.toml"
    )
    client = None
else:
    client = OpenAI(api_key=api_key)

# --- 3. CORE LOGIC FUNCTIONS ---

def extract_text_from_pdf(file):
    """Parses text from an uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def generate_ai_insights(document_text):
    """Sends text to OpenAI to generate summary and task breakdown in JSON format."""
    system_instruction = """
    You are an expert Business Analyst and Project Manager. 
    Analyze the provided document and return a structured JSON response.
    
    JSON Schema:
    {
      "project_summary": "A concise 3-5 sentence overview",
      "milestones": ["List of 3 key goals"],
      "tasks": [
        {"task": "Task name", "role": "e.g., Dev, QA, BA", "priority": "High/Med/Low", "description": "Short detail"}
      ]
    }
    """
    
    if client is None:
        st.error("OpenAI client not initialized. Please configure OPENAI_API_KEY.")
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Document content:\n{document_text}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Processing Error: {e}")
        return None

# --- 4. APP WORKFLOW ---

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    st.info("Ensure your OpenAI API Key is valid.")

# Main Upload Section
uploaded_file = st.file_uploader("Upload Project Document (PDF)", type="pdf")

if uploaded_file:
    if st.button("Generate Insights"):
        with st.spinner("Reading document and generating tasks..."):
            # Step A: Extraction
            raw_text = extract_text_from_pdf(uploaded_file)
            
            if raw_text:
                # Step B: AI Analysis
                data = generate_ai_insights(raw_text)
                
                if data:
                    st.success("Analysis Complete!")
                    
                    # Display Summary
                    st.subheader("📝 Project Summary")
                    st.write(data.get("project_summary", "No summary available."))
                    
                    # Display Milestones in columns
                    st.subheader("🎯 Key Milestones")
                    cols = st.columns(3)
                    for idx, milestone in enumerate(data.get("milestones", [])):
                        cols[idx % 3].info(milestone)
                    
                    # Display Task Table
                    st.subheader("✅ Task Breakdown")
                    st.table(data.get("tasks", []))
                    
                    # Optional: JSON Download for Jira/DevOps integration
                    st.download_button(
                        label="Download Tasks as JSON",
                        data=json.dumps(data, indent=2),
                        file_name="tasks.json",
                        mime="application/json"
                    )