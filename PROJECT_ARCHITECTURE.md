# AI Resume RAG System Architecture & Guide

Welcome to the comprehensive guide for the AI Resume RAG application you built! This document serves as a "notebook" to explore what is happening under the hood, so you understand the architecture, the code, and feel confident to recreate similar, or even more advanced, projects in the future.

---

## 1. High-Level Architecture Overview

At its core, this project builds a **Retrieval-Augmented Generation (RAG)** application. A traditional AI doesn't know who "Venkatesh" is. RAG solves this by first *Retrieving* relevant text from your resume, and then *Augmenting* the prompt so the AI can *Generate* an accurate, factual answer instead of making things up.

### The Stack:
- **Backend framework:** FastAPI (Python)
- **AI Integration:** OpenAI Python SDK (Using NVIDIA's DeepSeek model endpoint)
- **Vector / Retrieval:** Langchain framework & `BM25Retriever`
- **Memory Tracking:** Langchain's `InMemoryChatMessageHistory`
- **Frontend:** Vanilla HTML, CSS, JavaScript

---

## 2. File-by-File Code Breakdown

Let's dissect each Python file to understand what magic happens behind the scenes.

### `config.py`
**Purpose:** Handles all the environment variables and external API endpoints.
- **Workflow:** Reads secret keys from your `.env` file via `python-dotenv`.
- **Highlights:** Configures the base URL (`https://integrate.api.nvidia.com/v1`) to route requests to an NVIDIA-hosted model, specifically targeting `deepseek-ai/deepseek-v3.2` rather than OpenAI's default endpoints. It also loads email SMTP credentials for your contact form.

### `retriever.py`
**Purpose:** Turns your PDF Resume into searchable data.
- **Workflow:** 
  1. Uses Langchain's `PyPDFLoader` to parse text from `data/bandaruvenkateshrao_resume.pdf`.
  2. Converts the documents into a `BM25Retriever`. Instead of mathematical embeddings (AI embeddings), BM25 uses term frequency-inverse document frequency (TF-IDF) searching to find exact words and keyword matches quickly.
  3. Returns the `k=4` most relevant text chunks from the PDF.

### `memory.py`
**Purpose:** Remembers prior context in an ongoing conversation.
- **Workflow:** Maintains a simple global python dictionary (`store = {}`) mapping `session_id` to the session's chat history. 
- **Learning curve:** Right now the `InMemoryChatMessageHistory` wipes cleanly when you restart the server. In future, larger apps, you'd integrate Redis or a database (like PostgreSQL/MongoDB) for persistent memory.

### `main.py`
**Purpose:** The intelligent heart of your application.
- **Workflow:** 
  1. Initializes the `OpenAI` client pointing to NVIDIA's API.
  2. Defines the `ask_question()` function which:
     - Uses `retriever.invoke(question)` to find relevant chunks in the resume.
     - Formats those chunks into a `context` string.
     - Grabs the user's `session_id` history via `memory.py`.
     - Wraps everything in a strict `prompt`, telling the AI: "You are Venkatesh Virtually... use the context provided to answer".
     - Calls the LLM and extracts the AI's answer.
- **Bonus:** `if __name__ == "__main__":` block allows you to run `python main.py` directly in terminal to test the logic without starting the FastAPI server.

### `app.py`
**Purpose:** The Web Server (built with FastAPI).
- **Workflow:**
  - `FastAPI()` spins up the server instance. 
  - `app.mount("/data", ...)` exposes static images and pdfs to the frontend.
  - Defines **Pydantic Models** (`QuestionRequest`, `ContactRequest`). These ensure the data sent from the website perfectly matches the shape Python expects.
  - `@app.post("/ask")`: Receives the JSON query from frontend, sends it to `main.py` -> `ask_question()`, and returns the text response.
  - `@app.post("/contact")`: A neat endpoint that leverages `BackgroundTasks` to send emails via `smtplib` asynchronously. Your user gets a "Message Submitted" response *instantly* instead of waiting 3 seconds for Google's SMTP to send the email!
  - `@app.get("/")`: Triggers the server to render `index.html`.

---

## 3. The RAG Flow (Step-by-Step)

Here is exactly what happens when someone clicks "**SEND**" on the website:
1. **JavaScript:** Grabs user text input, disables the button, and sends a `POST` request to `http://localhost:8000/ask`.
2. **FastAPI (`app.py`):** Receives the `POST` request, validates the JSON shapes using Pydantic, calls `ask_question()`.
3. **Retrieval (`main.py` + `retriever.py`):** The `BM25Retriever` scans your PDF. It quickly finds the top 4 sentences matching the user's query keywords.
4. **Prompt Magic (`main.py`):** Compiles the context text + system instructions + the actual user question together into one big prompt sequence.
5. **LLM Invocation (`main.py`):** Calls the `deepseek-v3.2` model hosted on NVIDIA via the OpenAI SDK wrapper.
6. **Response loop:** Model returns text -> `app.py` sends it to the Frontend -> Javascript types it out letter by letter using an animation.

---

## 4. Learnings & Tips For Your Next Projects

Now that you've mastered this structure, here is how you can level up on your next AI builds:

**1. Migrate to Vector Embeddings:** 
In this project, you use `BM25Retriever` (keyword search). In your next project, try using embeddings (like `OpenAIEmbeddings` or HuggingFace embeddings) with a Vector Database like **ChromaDB**, **Pinecone**, or **Qdrant**. It will find semantic meaning (e.g., matching "programming" with "software development"), rather than strict keyword matches.

**2. State Management with SQL/Databases:**
Your current contact form sends emails cleanly, and `memory.py` uses temporary RAM. Next time, try implementing **SQLAlchemy** with **SQLite/PostgreSQL** to securely store Contact Form submissions into a database table.

**3. Move Frontend to React/Next.js:**
You have a beautiful, animated vanilla HTML/CSS frontend. As pages grow in complexity, consider writing your APIs with FastAPI, but building your UI via a library like React or Next.js to easily manage components instead of a 900-line `index.html` file.

**4. Advanced System Prompts:**
To expand your bot's intelligence, try supplying the system prompt with multiple dynamic tools (e.g., retrieving live weather, checking a database) using actual Langchain Agents framework rather than basic RAG chains.

### Congratulations! 🎉
You have fundamentally bridged the gap between front-end visuals, API engineering, AI engineering, and data retrieval. Keep experimenting!
