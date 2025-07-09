import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample
import pickle
from preprocess import clean_text

# Load dataset
df = pd.read_csv("data/clean_resume_data.csv").dropna()

# Clean the text
df["CleanedText"] = df["Feature"].apply(clean_text)

# Balance the dataset
max_count = df["Category"].value_counts().max()
balanced_data = []

for cat in df["Category"].unique():
    group = df[df["Category"] == cat]
    sampled = resample(group, replace=True, n_samples=max_count, random_state=42)
    balanced_data.append(sampled)

df_balanced = pd.concat(balanced_data)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df_balanced["CleanedText"], df_balanced["Category"], test_size=0.2, random_state=42
)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Classifier
model = RandomForestClassifier()
model.fit(X_train_tfidf, y_train)

# Evaluation on test set
y_pred = model.predict(X_test_tfidf)
test_accuracy = accuracy_score(y_test, y_pred)
print("\n📊 Test Set Accuracy:", round(test_accuracy * 100, 2), "%")
print(classification_report(y_test, y_pred))

# Evaluation on training set
y_train_pred = model.predict(X_train_tfidf)
train_accuracy = accuracy_score(y_train, y_train_pred)
print("\nTraining Score:", round(train_accuracy * 100, 2), "%")
print("\nTesting Score:", round(test_accuracy * 100, 2), "%")

# Save model
import os
os.makedirs("model", exist_ok=True)

with open("model/rf_classifier.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
