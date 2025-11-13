# 📰 منصة التحرير الإعلامي | Media Editing Platform

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![n8n](https://img.shields.io/badge/Backend-n8n-48A9A6?logo=n8n&logoColor=white)](https://n8n.io/)
[![Language](https://img.shields.io/badge/Language-Arabic%20(UTF--8)-blue)]()
[![LLM](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Pro-purple)](https://ai.google.dev/)

---

## 🧩 Overview

**منصة التحرير الإعلامي** (Media Editing Platform) is a comprehensive Arabic-language system that enables journalists and editors to:
1. **Rewrite raw text** according to selected editorial policies
2. **Generate AI-powered news anchor videos** with Arabic voice-over and lip-sync

The platform integrates **Streamlit** (frontend), **n8n** (backend automation), **Google Gemini 2.5 Pro** (LLM), and multiple AI services for video generation.

🎯 **Goal:**  
To automate the entire editorial workflow — from text rewriting to professional video generation — within one unified interface.

---

## 🧱 System Architecture

| Component | Description |
|------------|-------------|
| 🎨 **Frontend – Streamlit** | Web interface in Arabic for text input, editorial policy selection, and video generation. |
| ⚙️ **Backend – n8n** | Handles API requests, routing, prompt generation, and orchestrates the video pipeline. |
| 🧠 **LLM – Google Gemini 2.5 Pro** | Generates rewritten articles according to editorial rules and tone. |
| 🎙️ **ElevenLabs** | Arabic text-to-speech generation for news audio. |
| 👤 **AvatarTalk.ai** | Creates realistic Arabic news anchor video animations. |
| 🎬 **Sync.so (Wave2Lip)** | Lip-sync technology to sync audio with video. |
| 💾 **Google Drive** | Temporary storage for video and audio files during processing. |

---

## ⚙️ Workflow Steps

### 📝 Editorial Workflow (Text Rewriting)

1. **Webhook Node** → Receives `POST` request from Streamlit with policy and text.
2. **Switch Node** → Routes to appropriate policy (`najah_media`, `gaza_tv`, `najah_news`).
3. **Python Code Node** → Builds Arabic prompt template for selected policy.
4. **Google Gemini 2.5 Pro** → Generates rewritten text following editorial guidelines.
5. **JavaScript Code Node** → Parses and formats the output into structured sections.
6. **Respond to Webhook** → Returns formatted JSON to Streamlit.

### 🎬 Video Generation Workflow

1. **Webhook Node** → Receives news text and anchor description.
2. **Parallel Processing:**
   - **AvatarTalk.ai** → Generates video of Arabic news anchor
   - **ElevenLabs** → Generates Arabic voice-over audio
3. **Google Drive Upload** → Uploads both video and audio files
4. **File Sharing** → Makes files publicly accessible
5. **Sync.so (Wave2Lip)** → Merges video with audio for perfect lip-sync
6. **Status Monitoring** → Polls processing status with wait intervals
7. **Response** → Returns final video URL or error message

---

## 💻 Streamlit Frontend Features

### Text Rewriting Interface
- Text input area for raw Arabic content
- Three editorial policy buttons:
  - 🟢 **Najah Media** (Professional, analytical)
  - 🔵 **Gaza TV** (National, patriotic)
  - 🟣 **Najah News** (Journalistic, concise)
- Display of original and rewritten text side-by-side

### Video Generation Interface
- **Generate Video** button for rewritten news text
- **Test Video** button with sample content
- Video preview player with download option
- Real-time status updates and error handling
- Automatic retry logic for video processing

---

## 🖋️ Editorial Policies

| Policy             | Description                                                                           | Key Characteristics |
| ------------------ | ------------------------------------------------------------------------------------- | ------------------- |
| 🟢 **Najah Media** | Professional, neutral, analytical Arabic style for university media.                  | Objective, balanced, analytical |
| 🔵 **Gaza TV**     | National, human, and emotional tone highlighting Palestinian resilience and identity. | Patriotic, humanistic, resilient |
| 🟣 **Najah News**  | Journalistic, concise, factual reporting with chronological sequencing.               | Direct, timely, factual |

All outputs follow this structure:
```
التصنيف:
العنوان:
المقدمة:
التفاصيل:
الخاتمة:
```

---

## 🖼️ Screenshots

### 🧩 n8n Workflows

**Editorial Workflow:**
<img width="1174" height="231" alt="Editorial Workflow" src="https://github.com/user-attachments/assets/de525b63-e6bb-4436-8aeb-404608cb8755" />

**Video Generation Workflow:**
<img width="1152" height="181" alt="Video Pipeline" src="https://github.com/user-attachments/assets/fc47c63b-114e-4185-b936-a9739a476a8b" />

### 🖋️ Streamlit Interface
<img width="697" height="600" alt="Frontend Interface" src="https://github.com/user-attachments/assets/c5309f19-4f34-4319-bb87-5b6e1e0500b3" />

---

## 🚀 Setup Guide

### 1️⃣ Prerequisites

Install required Python packages:
```bash
pip install streamlit requests
```

### 2️⃣ Run n8n Backend

Using Docker:
```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Or locally:
```bash
n8n
```

Open in browser: `http://localhost:5678`

### 3️⃣ Import n8n Workflows

1. Navigate to n8n dashboard
2. Import both workflow JSON files:
   - `News_text_generation_workflow.json` (Editorial workflow)
   - `video_generation_workflow.json` (Video pipeline)
3. Configure API credentials (see below)
4. Activate both workflows
5. Note the webhook URLs:
   - Editorial: `http://localhost:5678/webhook-test/news-editor`
   - Video: `http://localhost:5678/webhook-test/uploadeverthing`

### 4️⃣ Run Streamlit Frontend

```bash
streamlit run app.py
```

Ensure webhook URLs in `app.py` match your n8n setup:
```python
# Editorial endpoint
url = "http://localhost:5678/webhook-test/news-editor"

# Video generation endpoint  
url = "http://localhost:5678/webhook-test/uploadeverthing"
```

---

## 🔑 Required API Credentials

You must obtain API keys for the following services:

| Service | Purpose | How to Get API Key |
| ------- | ------- | ------------------ |
| **Google Gemini API** | Text generation and rewriting | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| **ElevenLabs** | Arabic text-to-speech | [ElevenLabs API Keys](https://elevenlabs.io/app/developers/api-keys) |
| **AvatarTalk.ai** | Avatar video generation | [AvatarTalk API](https://avatartalk.ai/api-integration) |
| **Sync.so** | Video lip-sync (Wave2Lip) | [Sync.so Login](https://sync.so/login) |
| **Google Drive OAuth2** | File storage and sharing | [Google Cloud Console](https://console.cloud.google.com/) |

### Configuring Credentials in n8n

1. Go to **Settings** → **Credentials** in n8n
2. Add each credential with your API keys
3. Link credentials to respective nodes in both workflows
4. Test connections before activating workflows

> ⚠️ **Security Note:** Never commit API keys to version control. Use environment variables or n8n's credential system.

---

## 🧪 Example Usage

### Text Rewriting

1. Paste Arabic news text in the text area
2. Click one of the policy buttons (e.g., **سياسة Najah Media**)
3. View the rewritten text with proper structure
4. Copy or use the output as needed

### Video Generation

1. After rewriting text, click **توليد الفيديو من النص**
2. Wait 30-60 seconds for processing
3. Video appears with embedded player
4. Download video using the download button

### Test Mode

Use the **توليد فيديو تجريبي (اختبار)** button to test the video pipeline without rewriting text.

---

## 🧰 Technologies Used

| Category | Tools |
| -------- | ----- |
| **Frontend** | Streamlit (Python) |
| **Backend** | n8n Workflow Automation |
| **LLM** | Google Gemini 2.5 Pro |
| **TTS** | ElevenLabs API |
| **Avatar** | AvatarTalk.ai |
| **Lip-sync** | Sync.so (Wave2Lip v2) |
| **Storage** | Google Drive API |
| **Language** | Arabic (UTF-8) |
| **Format** | JSON, MP4, MP3 |

---

## 🧭 Project Structure

```
project/
│
├── app.py                                    # Streamlit frontend
├── N8N/
│   ├── News_text_generation_workflow.json   # Editorial rewriting workflow
│   └── video_generation_workflow.json       # Video generation pipeline
├── editorial flow photos/
│   ├── backend.png
│   └── frontend.png
└── README.md
```

---

## 🎯 Key Features

### Text Processing
- ✅ Three distinct editorial policies
- ✅ Automatic Arabic text structuring
- ✅ Google Gemini 2.5 Pro integration
- ✅ Real-time processing feedback

### Video Generation
- ✅ AI-generated Arabic news anchors
- ✅ Professional Arabic voice-over
- ✅ Automatic lip-sync technology
- ✅ Retry logic for failed generations
- ✅ Error handling and status messages
- ✅ Video download capability

---

## 🐛 Troubleshooting

### Video Generation Fails

1. **Check API keys** are valid and have sufficient credits
2. **Verify Google Drive permissions** allow file uploads
3. **Check network connectivity** to all external services
4. **Review n8n execution logs** for specific error messages
5. **Ensure wait time is sufficient** (30 seconds default)

### Common Issues

| Issue | Solution |
| ----- | -------- |
| Webhook timeout | Increase timeout in Streamlit requests |
| Arabic text encoding | Ensure UTF-8 encoding throughout |
| Video not loading | Check Google Drive file sharing permissions |
| Lip-sync quality poor | Verify audio and video resolution compatibility |

---

## 📺 Demo Video

Watch the platform in action: [Demo Video](https://drive.google.com/file/d/1AfGdTl4bCKZsB2DbzGAQ5CWYWYQl5RIZ/view?usp=sharing)

---

## 👥 Authors

**Developed by:**
- 👩‍💻 **Sama Shalabi**
- 👩‍💻 **Bissan Dwekat**
- 👩‍💻 **Rama Sabboubeh**

### Contributions:
- 🧠 n8n workflow design and integration
- 💻 Streamlit frontend development
- 🤖 LLM prompt engineering
- 🎬 Video pipeline architecture
- 📝 Arabic editorial policy implementation

---

## 📝 License

This project is developed for academic and research purposes at An-Najah National University.

---

## 🔮 Future Enhancements

- [ ] Support for multiple anchor avatars
- [ ] Batch processing for multiple articles
- [ ] Export to various video formats
- [ ] Integration with social media platforms
- [ ] Real-time collaborative editing
- [ ] Advanced video editing features
- [ ] Custom voice cloning options

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact the development team
- Check n8n community forums
- Review API documentation for each service

---

**Made with ❤️ for Arabic journalism and media innovation**
