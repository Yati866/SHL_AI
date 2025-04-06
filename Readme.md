# 📘 SHL RAG Assistant

**SHL RAG Assistant** is an intelligent tool designed to help users find the most relevant SHL assessments based on natural language queries. It uses **web scraping**, **semantic search** (via Sentence Transformers), and **Supabase** as a backend vector database — all wrapped in a sleek **Streamlit** frontend.

## 🚀 Features

- 🔍 Semantic search over SHL assessments (RAG-style)
- 🧠 Embedding-based matching using `all-MiniLM-L6-v2`
- 📊 Structured metadata: test type, duration, adaptive, remote-compatible
- 🌐 Streamlit frontend for user interaction
- ⚡ Real-time filtering and matching using Supabase vector RPC

---

## 🧩 Tech Stack

| Component     | Tool/Library                    |
|---------------|---------------------------------|
| Embedding     | [`sentence-transformers`](https://www.sbert.net/) |
| Frontend      | [`Streamlit`](https://streamlit.io/) |
| Backend DB    | [`Supabase`](https://supabase.com/) |
| Web Scraping  | `requests`, `beautifulsoup4`    |
| Deployment    | Streamlit Sharing |

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/shl-rag-assistant.git
   cd shl-rag-assistant
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up `.env` File**

   Create a `.env` file in the root with:
   ```env
   SUPABASE_URL=your-supabase-url
   SUPABASE_SERVICE_KEY=your-supabase-service-role-key
   ```

4. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 How It Works

- `scraper.py`: Crawls SHL's public product catalog and collects metadata like test types, duration, adaptive, etc.
- `embed_and_upload.py`: Converts each scraped test into a vector embedding using `sentence-transformers` and uploads it to Supabase (`products` table).
- `match_products` (Supabase RPC): Vector search procedure that finds semantically close results based on user input.
- `query_assessments.py`: Queries Supabase for top matches based on similarity threshold.
- `app.py`: Frontend in Streamlit allowing users to input natural queries and view the best-fit SHL assessments.

---

## 📁 Folder Structure

```
.
├── app.py                  # Streamlit frontend
├── query_assessments.py    # Vector-based search logic
├── scraper.py              # Web scraper for SHL assessments
├── embed_and_upload.py     # Embeds data and pushes to Supabase
├── individual_test_solutions.json  # Raw scraped data
├── requirements.txt
├── .env                    # Environment variables (not committed)
└── README.md
```

---

## 📊 Example Query

> _"Looking for a short adaptive personality test that works remotely."_

✅ Output will show:
- Relevant test name
- Duration
- Remote & Adaptive support
- Test type
- Direct SHL URL
- Similarity score

---

## ✅ To-Do / Improvements

- [ ] Add user authentication or analytics tracking (optional)
- [ ] Include summary generation for each assessment

---

## 🙌 Acknowledgements

- [SHL](https://www.shl.com/) for the rich catalog of assessments
- [Supabase](https://supabase.com/) for vector search capability
- [Sentence Transformers](https://www.sbert.net/) for embedding magic

---

## 📬 Contact

Built by **Ayush Gupta**

---