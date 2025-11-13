import streamlit as st
import requests

st.set_page_config(page_title="منصة التحرير الإعلامي", layout="wide")

# ---------------------------------
# Session state initialization
# ---------------------------------
if "response_data" not in st.session_state:
    st.session_state["response_data"] = None  # rewritten article from n8n
if "video_url" not in st.session_state:
    st.session_state["video_url"] = None  # final avatar video URL
if "error_msg_avatar" not in st.session_state:
    st.session_state["error_msg_avatar"] = None  # avatar pipeline error


# ---------------------------------
# Helper functions
# ---------------------------------
def call_n8n(policy_name: str, user_text: str):
    """
    Send the text + policy to n8n and return the JSON result
    of the rewriting step.
    """
    url = "http://localhost:5678/webhook-test/news-editor"
    payload = {
        "policy": policy_name,
        "text": user_text,
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def call_avatar_pipeline(news: str, anchor_description: str):
    """
    Send the rewritten Arabic text to the n8n avatar workflow.
    n8n should respond with { "video_url": "https://..." }.
    """
    url = "http://localhost:5678/webhook-test/uploadeverthing"
    payload = {
        "news_text": news,
        "anchor_description": anchor_description,
    }

    try:
        r = requests.post(url, json=payload, timeout=180)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


# ---------------------------------
# UI: Header
# ---------------------------------
st.title("منصة التحرير الإعلامي")
st.write("أدخل النص الخام، ثم اختر السياسة التحريرية لإعادة الصياغة، وبعدها يمكنك توليد فيديو المذيع.")

# ---------------------------------
# User input text area
# ---------------------------------
user_text = st.text_area(
    "النص الأصلي:",
    height=200,
    placeholder="ألصق هنا الخبر / البيان / النص الأولي باللغة العربية...",
)

st.write("---")
st.write("اختر السياسة التحريرية المطلوبة:")

col1, col2, col3 = st.columns(3)
error_msg = None

# ---------------------------------
# Policy buttons (rewrite)
# ---------------------------------
with col1:
    if st.button("سياسة Najah Media"):
        if not user_text.strip():
            error_msg = "الرجاء إدخال نص أولاً."
        else:
            data, err = call_n8n("najah_media", user_text)
            if err or not data:
                error_msg = "حصل خطأ أثناء الاتصال بالنظام."
            else:
                st.session_state["response_data"] = data
                st.session_state["video_url"] = None
                st.session_state["error_msg_avatar"] = None

with col2:
    if st.button("سياسة Gaza TV"):
        if not user_text.strip():
            error_msg = "الرجاء إدخال نص أولاً."
        else:
            data, err = call_n8n("gaza_tv", user_text)
            if err or not data:
                error_msg = "حصل خطأ أثناء الاتصال بالنظام."
            else:
                st.session_state["response_data"] = data
                st.session_state["video_url"] = None
                st.session_state["error_msg_avatar"] = None

with col3:
    if st.button("سياسة Najah News"):
        if not user_text.strip():
            error_msg = "الرجاء إدخال نص أولاً."
        else:
            data, err = call_n8n("najah_news", user_text)
            if err or not data:
                error_msg = "حصل خطأ أثناء الاتصال بالنظام."
            else:
                st.session_state["response_data"] = data
                st.session_state["video_url"] = None
                st.session_state["error_msg_avatar"] = None

st.write("---")

# ---------------------------------
# Show backend call error
# ---------------------------------
if error_msg:
    st.error(f"⚠️ {error_msg}")

# ---------------------------------
# Show original text
# ---------------------------------
st.subheader("📄 النص الأصلي")
if user_text.strip():
    st.write(user_text)
else:
    st.write("لم يتم إدخال نص بعد.")

st.write("---")

# ---------------------------------
# Display rewritten text
# ---------------------------------
if st.session_state["response_data"]:
    st.subheader("📰 النتيجة المعاد صياغتها")

    category = st.session_state["response_data"][0].get("category", "")
    title = st.session_state["response_data"][0].get("title", "")
    body = st.session_state["response_data"][0].get("clean_text", "")

    st.text(f"📍 {category}")
    st.title(title)
    st.write(body)

    st.write("---")

    # ---------------------------------
    # Avatar generation section (dynamic)
    # ---------------------------------
    st.subheader("🎬 إنشاء فيديو المذيع")

    # Get the rewritten text dynamically
    news_text = st.session_state["response_data"][0].get("news_text", "")
    if not news_text:
        # fallback to clean_text if news_text key is missing
        news_text = body

    default_anchor_prompt = (
        "مذيعة أخبار عربية ترتدي بدلة رسمية داكنة، إضاءة استوديو تلفزيوني، لقطة أمامية بوجه هادئ ومحايد"
    )

    if st.button("🎥 توليد الفيديو من النص المعاد صياغته"):
        with st.spinner("⏳ جاري إنشاء الفيديو عبر n8n، يرجى الانتظار..."):
            avatar_response, avatar_error = call_avatar_pipeline(
                news=news_text,
                anchor_description=default_anchor_prompt,
            )

        if avatar_error:
            st.session_state["error_msg_avatar"] = avatar_error
            st.error(f"حدث خطأ أثناء توليد الفيديو:\n{avatar_error}")
        else:
            # Handle both list or dict response formats
            if isinstance(avatar_response, list) and len(avatar_response) > 0:
                st.session_state["video_url"] = avatar_response[0].get("outputUrl") or avatar_response[0].get("video_url")
            else:
                st.session_state["video_url"] = avatar_response.get("outputUrl") or avatar_response.get("video_url")
            st.session_state["error_msg_avatar"] = None

# ---------------------------------
# Display Errors
# ---------------------------------
if st.session_state["error_msg_avatar"]:
    st.error(f"⚠️ حصل خطأ أثناء إنشاء الفيديو:\n{st.session_state['error_msg_avatar']}")

# ---------------------------------
# Display Video
# ---------------------------------
if st.session_state["video_url"]:
    st.write("---")
    st.subheader("🎥 الفيديو الناتج")

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.video(st.session_state["video_url"], format="video/mp4", start_time=0)
        st.write("")
        try:
            video_bytes = requests.get(st.session_state["video_url"]).content
            st.download_button(
                label="⬇️ تحميل الفيديو",
                data=video_bytes,
                file_name="edited_video.mp4",
                mime="video/mp4",
            )
        except Exception:
            st.warning("⚠️ تعذر تحميل الفيديو للتحميل المباشر.")
