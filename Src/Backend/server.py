import requests
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
from sentence_transformers import SentenceTransformer, util
import os
from dotenv import load_dotenv
from pdf_processor import extract_text_from_pdf, summarize_text

load_dotenv()
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load dataset
with open("jioemployee_dataset.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

questions = [item["question"] for item in qa_data]
answers = [item["answer"] for item in qa_data]

# Load Sentence-BERT model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
question_embeddings = embedding_model.encode(questions, convert_to_tensor=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return {"response": "Please type your question so I can help you."}

    # Step 1: Semantic similarity matching
    query_embedding = embedding_model.encode(user_message, convert_to_tensor=True)
    similarity_scores = util.cos_sim(query_embedding, question_embeddings)[0]
    best_match_idx = int(similarity_scores.argmax())
    best_score = float(similarity_scores[best_match_idx])

    print(f"🔍 Match: '{questions[best_match_idx]}' — Score: {best_score:.3f}")

    if best_score >= 0.75:
        return {"response": answers[best_match_idx]}

    # Step 2: Fallback to OpenRouter (GPT-4.1 Mini)
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
             "model": "openai/gpt-4.1-mini",
             "max_tokens": 512,  # important to avoid token limit error
             "messages": [
             {"role": "system", "content": "You are an HR assistant for Jio employees."},
             {"role": "user", "content": user_message}
            ],
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"].strip()
            return {"response": content}
        else:
            print("⚠️ Unexpected OpenRouter response format:", result)
            return {"response": "⚠️ Assistant returned an unexpected response."}

    except requests.exceptions.RequestException as e:
        print("❌ OpenRouter API Request Error:", e)
        return {"response": "⚠️ Connection to AI assistant failed. Check your API key or internet."}
    except Exception as e:
        print("❌ General OpenRouter Fallback Error:", e)
        return {"response": "⚠️ Something went wrong while processing your question."}

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"message": "Jio HR Chatbot is live and smart!"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        raw_text = extract_text_from_pdf(file_path)
        summary = summarize_text(raw_text)

        os.remove(file_path)

        return {
            "text": raw_text,
            "summary": summary
        }
    except Exception as e:
        print("❌ PDF Processing Error:", e)
        return {"error": "Failed to process the uploaded PDF."}
