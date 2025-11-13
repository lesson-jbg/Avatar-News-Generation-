import streamlit as st
import requests

st.set_page_config(page_title="منصة التحرير الإعلامي", layout="wide")

# ---------------------------------
# Session state initialization
# ---------------------------------
if "response_data" not in st.session_state:
    st.session_state["response_data"] = None

if "video_url" not in st.session_state:
    st.session_state["video_url"] = None

if "error_msg_avatar" not in st.session_state:
    st.session_state["error_msg_avatar"] = None


# ---------------------------------
# Helper functions
# ---------------------------------

def call_n8n(policy_name: str, user_text: str):
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
    Send the final edited Arabic script to the n8n avatar workflow.
    
    """
    url = "http://localhost:5678/webhook-test/uploadeverthing"
    payload = {
        "news_text": news,
        "anchor_description": anchor_description,
    }

    try:
        r = requests.post(url, json=payload, timeout=600)
        r.raise_for_status()
        response_data=r.json()
        # Check if response contains an error
        if response_data.get("error"):
            error_msg = response_data.get("message", "حدث خطأ غير معروف")
            return None, error_msg
            
        return response_data, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


# ---------------------------------
# UI: Header
# ---------------------------------

st.title("منصة التحرير الإعلامي")
st.write("أدخل النص الخام، ثم اختر السياسة التحريرية لإعادة الصياغة.")

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
# Policy Buttons
# ---------------------------------

with col1:
    if st.button("سياسة Najah Media"):
        if not user_text.strip():
            error_msg = "الرجاء إدخال نص أولاً."
        else:
            data, err = call_n8n("najah_media", user_text)
            if err or not data:
                error_msg = "حصل خطأ غير متوقع لم يتم ارسال جواب."
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
                error_msg = "حصل خطأ غير متوقع لم يتم ارسال جواب."
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
                error_msg = "حصل خطأ غير متوقع لم يتم ارسال جواب."
            else:
                st.session_state["response_data"] = data
                st.session_state["video_url"] = None
                st.session_state["error_msg_avatar"] = None

st.write("---")

if error_msg:
    st.error(f"حصل خطأ أثناء الاتصال بوحدة المعالجة الخلفية:\n{error_msg}")

# ---------------------------------
# Show the Original Text
# ---------------------------------
st.subheader("النص الأصلي")
if user_text.strip():
    st.write(user_text)
else:
    st.write("لم يتم إدخال نص بعد.")

st.write("---")

# ---------------------------------
# Show the rewritten text and avatar generator
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

    st.subheader("🎬 إنشاء فيديو المذيع")

    news = st.session_state["response_data"][0].get("news_text", "")

    default_anchor_prompt = "مذيعة أخبار عربية ترتدي بدلة رسمية داكنة، إضاءة استوديو تلفزيوني، لقطة أمامية بوجه هادئ ومحايد"

    if st.button("توليد الفيديو من النص"):
        with st.spinner("⏳ جاري إنشاء الفيديو، يرجى الانتظار..."):
            avatar_response, avatar_error = call_avatar_pipeline(
                news=news,
                anchor_description=default_anchor_prompt,
            )

        if avatar_error:
            st.session_state["error_msg_avatar"] = avatar_error
            st.error(f"حدث خطأ أثناء توليد الفيديو:\n{avatar_error}")
        else:
            # Check if backend returned an error in the response
            if avatar_response.get("error"):
                error_msg = avatar_response.get("message", "حدث خطأ غير معروف")
                st.session_state["error_msg_avatar"] = error_msg
                st.error(f"❌ {error_msg}")
            else:
                if isinstance(avatar_response, list) and len(avatar_response) > 0:
                    st.session_state["video_url"] = avatar_response[0].get("outputUrl")
                else:
                    st.session_state["video_url"] = avatar_response.get("outputUrl")
                st.session_state["error_msg_avatar"] = None

# ---------------------------------
# Auto-Test Button
# ---------------------------------
st.write("---")
st.subheader("🧪 اختبار تلقائي للفيديو")

default_anchor_prompt = "مذيعة أخبار عربية ترتدي بدلة رسمية داكنة، إضاءة استوديو تلفزيوني، لقطة أمامية بوجه هادئ ومحايد"

if st.button("توليد فيديو تجريبي (اختبار)"):
    with st.spinner("⏳ جاري إنشاء الفيديو التجريبي، يرجى الانتظار..."):
        avatar_response, avatar_error = call_avatar_pipeline(
            news="""فهم منصة نجاح مميزة أعيد تنظيم مهرجان التكنولوجيا والابتكار في نجاح بمشاركة عملاء، تكنولوجيون العمل وتحفيز روح الابتكار بين الشباب الفلسطيني""",
            anchor_description=default_anchor_prompt,
            video_url="https://drive.google.com/file/d/1z3u7LeGm1OIkxmA9Gub_E7oqRr7aF_fK/view?usp=sharing",
            audio_url="https://drive.google.com/file/d/1BOkYIlWVpSQeYtMd-2TG6GdMwsCM7NX9/view?usp=sharing"
        )

    if avatar_error:
        st.session_state["error_msg_avatar"] = avatar_error
        st.error(f"حدث خطأ أثناء توليد الفيديو:\n{avatar_error}")
    else:
        if isinstance(avatar_response, list) and len(avatar_response) > 0:
            st.session_state["video_url"] = avatar_response[0].get("outputUrl")
        else:
            st.session_state["video_url"] = avatar_response.get("outputUrl")
        st.session_state["error_msg_avatar"] = None

# ---------------------------------
# Show Errors (if any)
# ---------------------------------
if st.session_state["error_msg_avatar"]:
    st.error(f"حصل خطأ أثناء إنشاء الفيديو:\n{st.session_state['error_msg_avatar']}")

# ---------------------------------
# Show Video (smaller + download button)
# ---------------------------------
if st.session_state["video_url"]:
    st.write("---")
    st.subheader("🎥 الفيديو الناتج")

    # Centered smaller video (using columns)
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.video(st.session_state["video_url"], format="video/mp4", start_time=0)

        # Add spacing and download button
        st.write("")
        try:
            video_bytes = requests.get(st.session_state["video_url"]).content
            st.download_button(
                label="⬇️ تحميل الفيديو",
                data=video_bytes,
                file_name="edited_video.mp4",
                mime="video/mp4",
            )
        except Exception as e:
            st.warning("تعذر تحميل الفيديو للتحميل المباشر.")
