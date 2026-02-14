import streamlit as st
import os
import tempfile
from src.parser import ResumeParser
from src.rag_engine import RAGEngine
import pandas as pd
import plotly.express as px

# Validations
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = ""

st.set_page_config(page_title="Intelligent Resume Analyzer", layout="wide")

st.markdown("""
    <style>
    /* Main Background: Deep Blue Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #ffffff;
    }
    
    /* Typography */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-align: center;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #a8d0e6;
        margin-bottom: 40px;
        text-align: center;
        font-weight: 400;
    }
    
    /* Text Globals */
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, li {
        color: #ffffff !important;
    }
    .stTextInput > label, .stTextArea > label, .stFileUploader > label {
        color: #00d2ff !important;
        font-weight: 600;
    }
    small, .caption {
        color: #b0bfc6 !important;
    }
    
    /* Card Styling - Glassmorphism Dark */
    .card {
        padding: 25px;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    /* Inputs */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255,255,255,0.05);
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00d2ff;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b161b;
        border-right: 1px solid #1c2e36;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: #000000;
        border: none;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #00d2ff !important;
    }
    </style>
    <div class="main-title">Intelligent Resume Analyzer</div>
    <div class="sub-header">AI-Powered Screening & Matching System</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    # Check if key exists
    has_key = bool(os.environ.get("GROQ_API_KEY"))
    
    # Use expander to hide the key input
    with st.expander("API Settings", expanded=not has_key):
        api_key_input = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
        if api_key_input:
            os.environ["GROQ_API_KEY"] = api_key_input
            st.success("API Key saved for session")
    
    st.markdown("---")
    st.markdown("Upload your resume and a job description to get a detailed match analysis.")

# Initialize modules
parser = ResumeParser()
# We initialize RAG engine only when needed effectively, or check for key

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Job Description")
    job_description = st.text_area("Paste the Job Description here", height=300)

with col2:
    st.subheader("2. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

if st.button("Analyze Resume", type="primary"):
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not job_description:
        st.warning("Please provide a Job Description.")
    elif not uploaded_file:
        st.warning("Please upload a resume.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name

                # Parse Resume
                resume_text = parser.parse(tmp_path)
                
                # Cleanup temp file
                os.remove(tmp_path)
                
                # Initialize RAG Engine
                rag_engine = RAGEngine()
                
                # Validate if it's a resume
                with st.spinner("Verifying document type..."):
                    if not rag_engine.validate_resume(resume_text):
                        st.error("The uploaded document does not appear to be a valid Resume or CV. Please upload a valid resume.")
                        st.stop()
                
                # Analyze with RAG Engine
                analysis_result = rag_engine.analyze_resume(resume_text, job_description)

                # Display Results
                st.success("Analysis Complete!")
                
                # Display Score
                score = analysis_result.get("match_score", 0)
                st.metric(label="Match Score", value=f"{score}/100")
                
                # Progress Bar
                st.progress(score / 100)
                
                # Detailed Breakdown with Radar Chart
                breakdown = analysis_result.get("match_breakdown", {})
                if breakdown:
                    st.divider()
                    st.subheader("Match Analysis Visualization")
                    
                    # Create DataFrame for Plotly
                    data = pd.DataFrame(dict(
                        r=[
                            breakdown.get('skills_match', 0),
                            breakdown.get('experience_match', 0),
                            breakdown.get('education_match', 0),
                            breakdown.get('communication_style', 0),
                            breakdown.get('skills_match', 0) # Close the loop
                        ],
                        theta=['Skills', 'Experience', 'Education', 'Communication', 'Skills']
                    ))
                    
                    fig = px.line_polar(data, r='r', theta='theta', line_close=True, range_r=[0, 100])
                    fig.update_traces(fill='toself', line_color='#00CC96')
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100])
                        ),
                        showlegend=False,
                        height=400,
                        margin=dict(l=40, r=40, t=20, b=20)
                    )
                    
                    # Display Chart and Metrics side-by-side
                    viz_col1, viz_col2 = st.columns([1.5, 1])
                    with viz_col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with viz_col2:
                        st.caption("Score Breakdown")
                        st.progress(breakdown.get('skills_match', 0) / 100, text=f"Skills: {breakdown.get('skills_match', 0)}%")
                        st.progress(breakdown.get('experience_match', 0) / 100, text=f"Experience: {breakdown.get('experience_match', 0)}%")
                        st.progress(breakdown.get('education_match', 0) / 100, text=f"Education: {breakdown.get('education_match', 0)}%")
                        st.progress(breakdown.get('communication_style', 0) / 100, text=f"Communication: {breakdown.get('communication_style', 0)}%")
                
                # Resume Improvements
                improvements = analysis_result.get("resume_improvements", [])
                if improvements:
                    st.divider()
                    st.subheader("Resume Refinement Suggestions")
                    for item in improvements:
                        with st.expander(f"Improvement for: {item.get('section', 'General')}"):
                            st.write(f"**Suggestion:** {item.get('suggestion')}")
                            st.info(f"**Example Rewrite:** {item.get('example')}")

                # Layout for details
                st.divider()
                st.subheader("Skills Analysis")
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.info("### Matching Skills")
                    for skill in analysis_result.get("matching_skills", []):
                        st.write(f"- {skill}")

                with res_col2:
                    st.warning("### Missing Skills")
                    for skill in analysis_result.get("missing_skills", []):
                        st.write(f"- {skill}")
                
                st.divider()
                st.subheader("Summary")
                st.markdown(f"""
                <div class="card">
                    {analysis_result.get("summary", "No summary available.")}
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader("Recommendation")
                rec = analysis_result.get("recommendation", "N/A")
                if rec.lower() == "hire":
                    st.success(f"**{rec}**")
                elif rec.lower() == "interview":
                    st.warning(f"**{rec}**")
                else:
                    st.error(f"**{rec}**")
                
                questions = analysis_result.get("interview_questions", [])
                if questions:
                    st.divider()
                    st.subheader("Interview Preparation Hub")
                    st.markdown("ask specific questions tailored to your profile to help you **crack the interview**.")
                    
                    for i, item in enumerate(questions, 1):
                        # Handle both simple string (fallback) and new dict format
                        if isinstance(item, str):
                            q_text = item
                            q_context = "General fit"
                            q_tip = "Use the STAR method (Situation, Task, Action, Result) to structure your answer."
                        else:
                            q_text = item.get("question", "Question")
                            q_context = item.get("context", "Relevant to your background")
                            q_tip = item.get("answer_tip", "Be confident and concise.")

                        with st.expander(f"**Q{i}: {q_text}**"):
                            st.markdown(f"**Why this question?**\n\n_{q_context}_")
                            st.info(f"**Pro Tip:** {q_tip}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                import traceback
                st.text(traceback.format_exc())
