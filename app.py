import streamlit as st
import pandas as pd

from utils.extract import extract_text_from_pdf, extract_name, extract_skills_from_resume
from utils.recommend import get_top_jobs

# Load job dataset
job_df = pd.read_csv("data/jobs_dataset_with_features.csv")

st.set_page_config(page_title="Job Recommendation", layout="centered")
st.title("📄 Resume-Based Job Recommender")

uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded)
        name = extract_name(text)
        skills = extract_skills_from_resume(text)
        top_jobs = get_top_jobs(skills, job_df, top_n=1)  # Only top 1 job

    st.success(" Analysis complete!")

    st.markdown(f"### Name: **{name}**")

    st.markdown("### Extracted Skills:")
    if skills:
        st.markdown("✅ " + ", ".join(skills))
    else:
        st.warning("No relevant skills found.")

    st.markdown("## Top Job Recommendation:")

    if not top_jobs.empty:
        row = top_jobs.iloc[0]
        st.markdown(f"####  **{row['Role']}**")
        st.markdown(f"[🔗 Apply on LinkedIn]({row['Link']})", unsafe_allow_html=True)
    else:
        st.warning("No suitable job found.")
