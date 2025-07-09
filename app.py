import streamlit as st
import pandas as pd
import os
import gdown

st.set_page_config(page_title="Job Recommendation", layout="centered")
st.title("📄 Resume-Based Job Recommender")

# Google Drive dataset link
csv_url = "https://drive.google.com/uc?id=1--bUAeQBYqc-rtZytUrjODVZVJ_6Ywnj"
csv_path = "data/jobs_dataset_with_features.csv"
os.makedirs("data", exist_ok=True)

@st.cache_data(show_spinner=False)
def load_dataset():
    if not os.path.exists(csv_path):
        gdown.download(csv_url, csv_path, quiet=False)
    return pd.read_csv(csv_path)

# File uploader
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded:
    with st.spinner("🔄 Loading dataset..."):
        try:
            job_df = load_dataset()
        except Exception as e:
            st.error("❌ Failed to load job dataset.")
            st.exception(e)
            st.stop()

    # ✅ Delayed imports — only after resume is uploaded
    from utils.extract import extract_text_from_pdf, extract_name, extract_skills_from_resume
    from utils.recommend import get_top_jobs

    try:
        with st.spinner("🧠 Analyzing resume..."):
            text = extract_text_from_pdf(uploaded)
            name = extract_name(text)
            skills = extract_skills_from_resume(text)
            top_jobs = get_top_jobs(skills, job_df, top_n=1)

        st.success("✅ Analysis complete!")

        st.markdown(f"### 👤 Name: **{name}**")
        st.markdown("### 🧠 Extracted Skills:")
        st.markdown("✅ " + ", ".join(skills) if skills else "⚠️ No relevant skills found.")

        st.markdown("## 💼 Top Job Recommendation:")
        if not top_jobs.empty:
            job = top_jobs.iloc[0]
            st.markdown(f"#### **{job['Role']}**")
            st.markdown(f"[🔗 Apply on LinkedIn]({job['Link']})", unsafe_allow_html=True)
        else:
            st.warning("No suitable job found.")

    except Exception as e:
        st.error("❌ Resume analysis failed.")
        st.exception(e)
