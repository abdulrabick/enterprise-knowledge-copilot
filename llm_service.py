
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_answer(question, search_results):
    """Generate an answer grounded in retrieved document text."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "API key not found. Check your .env file."

    if not search_results:
        return "No relevant document information was found."

    context_parts = []

    for result in search_results:
        filename = result["filename"]
        text = result["text"]

        context_parts.append(
            f"Source: {filename}\nContent: {text}"
        )

    context = "\n\n".join(context_parts)

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise knowledge assistant. "
                        "Answer questions using only the provided document "
                        "context. If the context does not contain the answer, "
                        "say that the information was not found in the "
                        "uploaded documents. Cite the source filename."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Document context:\n{context}\n\n"
                        f"Question: {question}"
                    ),
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"Could not generate an AI answer: {error}"

