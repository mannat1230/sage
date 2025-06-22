import gradio as gr
import shutil
import tempfile
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import extract_text_from_pdf
from src.summarizer import generate_summary

global_pdf_text = ""  # Store uploaded PDF text in memory

def upload_and_summarize(file):
    global global_pdf_text

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        shutil.copyfile(file.name, tmp_file.name)
        tmp_path = tmp_file.name

    global_pdf_text = extract_text_from_pdf(tmp_path)
    summary = generate_summary(global_pdf_text, context="Summarize the entire research paper.")
    return summary


def chat_with_pdf(message, history):
    global global_pdf_text
    if not global_pdf_text:
        return "Please upload a paper first."
    
    context = f"Answer the question below using the following research paper:\n\n{global_pdf_text[:3000]}"
    user_prompt = f"{context}\n\nQuestion: {message}"
    return generate_summary(global_pdf_text, context=f"Question: {message}")

with gr.Blocks() as demo:
    gr.Markdown("# 📄 SAGE – AI Research Assistant")
    gr.Markdown("Upload a research paper (PDF), and then chat with it like a research assistant.")

    with gr.Row():
        file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        summary_output = gr.Textbox(label="Initial Summary")

    with gr.Row():
        chatbot = gr.ChatInterface(chat_with_pdf)

    file_input.change(fn=upload_and_summarize, inputs=file_input, outputs=summary_output)

if __name__ == "__main__":
    demo.launch()
