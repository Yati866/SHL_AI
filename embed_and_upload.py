import streamlit as st
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

# Initialize Supabase client
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data from individual_test_solutions.json
with open("individual_test_solutions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Embed and upload each item
for item in data:
    try:
        # Prepare text for embedding (combine name and test types)
        description = item["name"] + " " + " ".join(item.get("test_types", []))
        embedding = model.encode([description])[0].tolist()

        payload = {
            "name": item["name"],
            "url": item["url"],
            "remote_testing": item.get("remote_testing"),
            "adaptive_irt": item.get("adaptive_irt"),
            "duration": item.get("Duration", "Unknown"),
            "test_types": ", ".join(item.get("test_types", [])),
            "embedding": embedding,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        response = supabase.table("products").insert(payload).execute()

        if response.data:
            print(f"✅ Inserted: {item['name']}")
        else:
            print(f"❌ Failed to insert: {item['name']}")

    except Exception as e:
        print(f"❌ Error processing {item['name']}: {e}")
