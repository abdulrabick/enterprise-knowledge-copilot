# AI Enterprise Knowledge Intelligence & Decision Copilot

## Overview

An AI-powered document assistant that allows users to upload company documents and ask questions about their contents.

## Features

* Upload PDF, DOCX, and TXT documents.
* Extract text from uploaded documents.
* Split documents into searchable sections.
* Use Sentence Transformers to generate embeddings.
* Search relevant sections using FAISS.
* Generate answers using the Groq API.
* Display retrieved source documents.

## Technology Stack

* Python
* Streamlit
* Sentence Transformers
* FAISS
* Groq API
* Python-dotenv

## Installation

1. Clone this repository.

2. Create and activate a Python virtual environment.

3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file in the project directory.

5. Add your Groq API key:

   `GROQ_API_KEY=your_groq_api_key`

6. Run the application:

   `python -m streamlit run app.py`

## Security

Keep API keys private. Never upload your `.env` file to GitHub.
