import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_jobs(candidate_skills, job_df, top_n=3):
    job_df = job_df.copy()
    job_df["CombinedSkills"] = job_df["Features"].fillna("").apply(str.lower)
    candidate_profile = " ".join(candidate_skills).lower()

    # TF-IDF & cosine similarity
    texts = job_df["CombinedSkills"].tolist() + [candidate_profile]
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(texts)
    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    job_df["MatchScore"] = similarities * 100

    # Create LinkedIn apply link
    job_df["Link"] = job_df["Role"].apply(
        lambda role: f"https://www.linkedin.com/jobs/search/?keywords={role.replace(' ', '%20')}"
    )

    return job_df.sort_values("MatchScore", ascending=False).head(top_n)
