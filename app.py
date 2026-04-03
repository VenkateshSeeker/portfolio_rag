import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import config
from main import ask_question

app = FastAPI(title="Resume RAG API")

app.mount("/data", StaticFiles(directory="data"), name="data")

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"

class AnswerResponse(BaseModel):
    answer: str

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

def send_contact_emails(name: str, user_email: str, message: str):
    try:
        smtp_server = "smtp.gmail.com"
        port = 465
        sender = config.EMAIL_SENDER
        password = config.EMAIL_APP_PASSWORD
        notify_target = config.EMAIL_NOTIFY_TARGET

        # 1. Notify the owner
        msg_notify = EmailMessage()
        msg_notify.set_content(f"New contact form submission!\n\nName: {name}\nEmail: {user_email}\nMessage:\n{message}")
        msg_notify["Subject"] = f"New Contact from {name}"
        msg_notify["From"] = sender
        msg_notify["To"] = notify_target

        # 2. Auto-reply to visitor
        msg_reply = EmailMessage()
        msg_reply.set_content(f"Hi {name},\n\nThank you for reaching out! I have received your message and will get back to you shortly.\n\nBest regards,\nVenkatesh")
        msg_reply["Subject"] = "Thank you for contacting me!"
        msg_reply["From"] = sender
        msg_reply["To"] = user_email

        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender, password)
            server.send_message(msg_notify)
            server.send_message(msg_reply)
    except Exception as e:
        print(f"Error sending email: {e}")

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    try:
        answer = ask_question(request.question, request.session_id)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
async def contact_form(request: ContactRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_contact_emails, request.name, request.email, request.message)
    return {"status": "success", "detail": "Message submitted"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
