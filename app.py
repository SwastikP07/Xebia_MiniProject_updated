import streamlit as st
import pandas as pd
import os
import gdown

# App Config
st.set_page_config(page_title="Job Recommendation", layout="centered")
st.title("📄 Resume-Based Job Recommender")

# Google Drive CSV setup
drive_url = "https://drive.google.com/uc?id=1--bUAeQBYqc-rtZytUrjODVZVJ_6Ywnj"
csv_path = "data/jobs_dataset_with_features.csv"

# Make sure data folder exists
os.makedirs("data", exist_ok=True)

# Lazy-load CSV
@st.cache_data(show_spinner=False)
def load_jobs_dataset():
    if not os.path.exists(csv_path):
        gdown.download(drive_url, csv_path, quiet=False)
    return pd.read_csv(csv_path)

# Resume uploader
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("🔁 Loading job dataset..."):
        try:
            job_df = load_jobs_dataset()
        except Exception as e:
            st.error("❌ Failed to load job dataset.")
            st.exception(e)
            st.stop()

    from utils.extract import extract_text_from_pdf, extract_name, extract_skills_from_resume
    from utils.recommend import get_top_jobs

    try:
        with st.spinner("🔍 Analyzing resume..."):
            text = extract_text_from_pdf(uploaded)
            name = extract_name(text)
            skills = extract_skills_from_resume(text)
            top_jobs = get_top_jobs(skills, job_df, top_n=1)

        st.success("✅ Analysis complete!")
        st.markdown(f"### 👤 Name: **{name}**")

        st.markdown("### 🧠 Extracted Skills:")
        if skills:
            st.markdown("✅ " + ", ".join(skills))
        else:
            st.warning("No relevant skills found in the resume.")

        st.markdown("## 🎯 Top Job Recommendation:")
        if not top_jobs.empty:
            row = top_jobs.iloc[0]
            st.markdown(f"#### 💼 **{row['Role']}**")
            st.markdown(f"[🔗 Apply on LinkedIn]({row['Link']})", unsafe_allow_html=True)
        else:
            st.warning("No suitable job found for your skills.")

    except Exception as e:
        st.error("❌ Something went wrong while processing your resume.")
        st.exception(e)
