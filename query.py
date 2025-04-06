# query_assessments.py

from sentence_transformers import SentenceTransformer
import streamlit as st
import numpy as np
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Initialize the model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Embed function
def embed(text):
    embedding = model.encode(text)
    return embedding.tolist()  # Supabase expects a list, not a NumPy array

# ✅ Initialize Supabase client
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ✅ Querying function
def query_recommendations(user_query, threshold=0.4, top_k=10):
    query_vector = embed(user_query)
    response = supabase.rpc("match_products", {
        "query_embedding": query_vector,
        "match_threshold": threshold,
        "match_count": top_k
    }).execute()

    return response.data

# # ✅ Example usage
# if __name__ == "__main__":
#     user_input = "Hiring for Python and SQL developer with good reasoning skills"
#     results = query_recommendations(user_input)

#     print(f"\n🔍 Results for: {user_input}\n")
#     for res in results:
#         print(f"✅ {res['name']} - {res['url']} (Similarity: {res['similarity']:.2f})")
#         print(f"   🧪 Test Type: {res['test_types']} | ⏱ Duration: {res['duration']}")
#         print(f"   🌐 Remote Testing: {res['remote_testing']} | 📊 Adaptive/IRT: {res['adaptive_irt']}\n")

