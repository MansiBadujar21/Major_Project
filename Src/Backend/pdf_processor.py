import fitz  # PyMuPDF
import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=800):  # chunks
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text):
    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "max_tokens": 200,  # shorter responses
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional document summarizer. "
                        "Generate a short, concise summary that captures only the key intent "
                        "and main points of the document. Do not include all bullet points or every section—"
                        "just the core idea in a few sentences."
                    )
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n{chunk}"
                }
            ]
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            result = res.json()

            if "choices" in result and result["choices"]:
                summaries.append(result["choices"][0]["message"]["content"].strip())
            else:
                summaries.append("[Summary failed: unexpected response format]")

        except Exception as e:
            print("❌ OpenRouter summarization error:", e)
            summaries.append("[Summary failed due to error]")

    return " ".join(summaries)
