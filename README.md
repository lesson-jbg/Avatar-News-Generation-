# 📰 منصة التحرير الإعلامي | Media Editing Platform

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![n8n](https://img.shields.io/badge/Backend-n8n-48A9A6?logo=n8n&logoColor=white)](https://n8n.io/)
[![Language](https://img.shields.io/badge/Language-Arabic%20(UTF--8)-blue)]()
[![LLM](https://img.shields.io/badge/AI-OpenRouter%20LLM-purple)](https://openrouter.ai/)

---


## 🧩 Overview

**منصة التحرير الإعلامي** (Media Editing Platform) is an Arabic-language system that allows journalists and editors to paste raw text and instantly rewrite it according to a selected **editorial policy**.  
It integrates **Streamlit** (frontend) with **n8n** (backend automation) and an **LLM (OpenRouter)** for high-quality Arabic rewriting.

🎯 **Goal:**  
To make the entire editorial rewriting process happen automatically within one unified interface — from text input to professionally restructured output.

---

## 🧱 System Architecture

| Component | Description |
|------------|-------------|
| 🎨 **Frontend – Streamlit** | Web interface in Arabic for text input, selecting editorial policy, and displaying results. |
| ⚙️ **Backend – n8n** | Handles incoming API requests, routing, and prompt creation for each editorial policy. |
| 🧠 **LLM – OpenRouter Model** | Generates the rewritten article according to the requested editorial rules and tone. |

---

## ⚙️ Workflow Steps

### 🧠 n8n Workflow
1. **Webhook Node** → Receives `POST` request from Streamlit.
2. **Switch Node** → Checks `policy` field (`najah_media`, `gaza_tv`, `najah_news`).
3. **Code in Python (Beta)** → Dynamically builds the Arabic prompt template for the selected policy.
4. **Basic LLM Chain** → Sends the prompt to OpenRouter LLM and gets rewritten text.
5. **Respond to Webhook** → Returns a structured JSON response to Streamlit.

### 💻 Streamlit Frontend
1. User pastes Arabic text.
2. Chooses one of the editorial policies:
   - 🟢 Najah Media  
   - 🔵 Gaza TV  
   - 🟣 Najah News  
3. Streamlit sends a JSON request to n8n:
```json
   {
     "policy": "najah_media",
     "text": "أعلنت وزارة التعليم العالي الفلسطينية ..."
   }
```

4. The rewritten structured article is returned and displayed in Arabic format:

```
   التصنيف:
   العنوان:
   المقدمة:
   التفاصيل:
   الخاتمة:
```

---

## 🖋️ Example Response

```json
{
  "text": "التصنيف: تعليمي – بحث علمي وتنمية\n\nالعنوان: وزارة التعليم العالي تطلق برنامج دعم البحث العلمي في الجامعات الفلسطينية\n\nالمقدمة: أعلنت وزارة التعليم العالي الفلسطينية عن إطلاق برنامج جديد..."
}
```

---

## 🧾 Editorial Policies

| Policy             | Description                                                                           |
| ------------------ | ------------------------------------------------------------------------------------- |
| 🟢 **Najah Media** | Professional, neutral, analytical Arabic style for university media.                  |
| 🔵 **Gaza TV**     | National, human, and emotional tone highlighting Palestinian resilience and identity. |
| 🟣 **Najah News**  | Journalistic, concise, factual reporting with chronological sequencing.               |

All outputs strictly follow the structure:

```
التصنيف:
العنوان:
المقدمة:
التفاصيل:
الخاتمة:
```

---

## 🧠 Example Prompt Logic (Python Node)

Each policy builds a distinct Arabic instruction template. Example for *Najah Media*:

```python

prompt = f"""
أنت محرر يعمل في مركز الإعلام – جامعة النجاح الوطنية.
المطلوب: إعادة صياغة النص بأسلوب عربي فصيح، مهني، وموضوعي.

النص: {_input.item.json.body.text}

التزم بالهيكل التالي:
التصنيف:
العنوان:
المقدمة:
التفاصيل:
الخاتمة:
"""
return { "prompt": prompt }

```

---

## 🖼️ Screenshots

### 🧩 n8n Workflow

<img width="1109" height="374" alt="backend" src="https://github.com/user-attachments/assets/87b1ad9e-7f02-4e92-8cec-9ca4dc67c07e" />

### 🖋️ Streamlit Interface
<img width="697" height="600" alt="frontend" src="https://github.com/user-attachments/assets/c5309f19-4f34-4319-bb87-5b6e1e0500b3" />

---

## 🚀 Setup Guide

### 1️⃣ Run n8n Backend

Using Docker:

```bash

docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

```

or locally 
```
n8n
```

Open in browser:

```
http://localhost:5678
```
n8n work flow : 
[My workflow.json](https://github.com/user-attachments/files/23150459/My.workflow.json)

* Activate the workflow.
* Copy the production Webhook URL:

```
http://localhost:5678/webhook/news-editor
```

---

### 2️⃣ Run Streamlit Frontend

Install dependencies:

```bash
pip install streamlit requests
```

Run the app:

```bash
streamlit run app.py
```

Ensure the backend URL matches:

```python
url = "http://localhost:5678/webhook/news-editor"
```

---

## 🧪 Example Usage

1. Paste your Arabic text in the text box.
2. Click **سياسة Najah Media** (or another policy).
3. Wait for processing.
4. View the rewritten text directly in the Streamlit interface.

---

## 🧰 Technologies Used

| Category | Tools              |
| -------- | ------------------ |
| Frontend | Streamlit (Python) |
| Backend  | n8n                |
| AI Model | OpenRouter LLM     |
| Language | Arabic (UTF-8)     |
| Format   | JSON               |

---

## 🧭 Project Structure

```
project/
│
├── app.py                     # Streamlit frontend
├── news-editor-workflow.json  # n8n workflow definition
├── editorial flow photos/
│   ├── backend.png
│   └── frontend.png
└── README.md
```

---

## 👥 Authors

**Developed by:**
👩‍💻 *Sama shalabi*
👩‍💻 *Bissan Dwekat*


* 🧠 Workflow design (n8n)
* 💻 Frontend implementation (Streamlit)
* 🤖 LLM integration (OpenRouter)

### 🔑 Required API Credentials

You must create accounts and get API keys for the following services used in the avatar and audio generation pipeline:

| Service                   | Purpose                                                             | Link to Get API Key                                                                                                                                                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **ElevenLabs**            | Text-to-speech (Arabic voice generation)                            | [https://elevenlabs.io/app/developers/api-keys](https://elevenlabs.io/app/developers/api-keys)                                                                                                                                                                                 |
| **AvatarTalk**            | Avatar animation and lip-sync                                       | [https://avatartalk.ai/api-integration](https://avatartalk.ai/api-integration)                                                                                                                                                                                                 |
| **Sync.so**               | Video rendering and merging service                                 | [https://sync.so/login](https://sync.so/login)                                                                                                                                                                                                                                 |
| **Google Drive (OAuth2)** | Used to access Google Drive links and files for video/audio storage | [https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/?utm_source=n8n_app&utm_medium=credential_settings&utm_campaign=create_new_credentials_modal#enable-apis) |

> 💡 **Note:** If the video generation doesn’t work, verify that your API keys are active and configured correctly inside your n8n workflow environment variables.
>
> demo video : https://drive.google.com/file/d/1AfGdTl4bCKZsB2DbzGAQ5CWYWYQl5RIZ/view?usp=sharing
