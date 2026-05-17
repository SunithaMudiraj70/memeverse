import streamlit as st
import requests

BASE_URL = "https://memeverse-xhbx.onrender.com"

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="😂 MemeVerse",
    page_icon="😂",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #141E30,
            #243B55
        );
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        color: white;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #dddddd;
        margin-bottom: 30px;
    }

    .card {
        background: rgba(255,255,255,0.08);
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(
            to right,
            #ff416c,
            #ff4b2b
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# TITLE
# =========================================

st.markdown(
    """
    <div class='main-title'>
    😂 MemeVerse
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    AI Powered Joke Generator 🚀
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# SIDEBAR
# =========================================

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "🏠 Home",
        "➕ Add Joke",
        "😂 Get Jokes",
        "🎲 Random Joke",
        "🤖 AI Joke Generator",
        "🔍 Search Joke",
        "✏️ Update Joke",
        "🗑️ Delete Joke",
        "📤 Upload File"
    ]
)

# =========================================
# HOME
# =========================================

if menu == "🏠 Home":

    st.markdown(
        """
        <div class='card'>
        <h1>😂 Welcome to MemeVerse</h1>

        <p>
        A funny AI powered joke platform built using FastAPI + Streamlit 🚀
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# ADD JOKE
# =========================================

elif menu == "➕ Add Joke":

    st.subheader("➕ Add Your Joke")

    joke = st.text_area(
        "Write your joke 😂"
    )

    if st.button("Add Joke"):

        response = requests.post(
            f"{BASE_URL}/jokes",
            json={
                "joke": joke
            }
        )

        if response.status_code == 200:

            st.success(
                "Joke Added Successfully 🎉"
            )

        else:

            st.error(
                "Failed to add joke"
            )

# =========================================
# GET JOKES
# =========================================

elif menu == "😂 Get Jokes":

    st.subheader("😂 All Posted Jokes")

    try:

        response = requests.get(
            f"{BASE_URL}/get-jokes"
        )

        jokes = response.json()

        if len(jokes) == 0:

            st.warning(
                "No jokes available 😢"
            )

        else:

            st.success(
                f"{len(jokes)} jokes found 🎉"
            )

            for joke in jokes:

                if isinstance(joke, dict):

                    joke_id = joke.get("id", "N/A")

                    joke_text = joke.get(
                        "joke",
                        "No joke found"
                    )

                    st.markdown(
                        f"""
                        <div class='card'>
                        <h3>🤣 Joke #{joke_id}</h3>
                        <p style='font-size:22px'>
                        {joke_text}
                        </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class='card'>
                        <p>{joke}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as e:

        st.error(
            f"Error loading jokes: {e}"
        )

# =========================================
# RANDOM JOKE
# =========================================

elif menu == "🎲 Random Joke":

    st.subheader("🎲 Random Joke")

    if st.button("Generate Random Joke 😂"):

        response = requests.get(
            f"{BASE_URL}/random-joke"
        )

        data = response.json()

        st.markdown(
            f"""
            <div class='card'>
            <h2>🤣 Random Joke</h2>
            <p style='font-size:24px'>
            {data.get('joke')}
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================
# AI JOKE
# =========================================

elif menu == "🤖 AI Joke Generator":

    st.subheader("🤖 AI Joke Generator")

    if st.button("Generate AI Joke 🚀"):

        response = requests.get(
            f"{BASE_URL}/ai-joke"
        )

        data = response.json()

        st.markdown(
            f"""
            <div class='card'>
            <h2>🤣 AI Joke</h2>
            <p style='font-size:24px'>
            {data.get('ai_joke')}
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================
# SEARCH
# =========================================

elif menu == "🔍 Search Joke":

    keyword = st.text_input(
        "Enter keyword"
    )

    if st.button("Search"):

        response = requests.get(
            f"{BASE_URL}/search?keyword={keyword}"
        )

        jokes = response.json()

        if jokes:

            for joke in jokes:

                st.markdown(
                    f"""
                    <div class='card'>
                    <p style='font-size:22px'>
                    {joke.get('joke')}
                    </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "No jokes found"
            )

# =========================================
# UPDATE
# =========================================

elif menu == "✏️ Update Joke":

    joke_id = st.number_input(
        "Joke ID",
        min_value=1
    )

    updated_joke = st.text_area(
        "Updated Joke"
    )

    if st.button("Update Joke"):

        response = requests.put(
            f"{BASE_URL}/jokes/{joke_id}",
            json={
                "joke": updated_joke
            }
        )

        st.success(
            response.json()["message"]
        )

# =========================================
# DELETE
# =========================================

elif menu == "🗑️ Delete Joke":

    joke_id = st.number_input(
        "Joke ID",
        min_value=1
    )

    if st.button("Delete Joke"):

        response = requests.delete(
            f"{BASE_URL}/jokes/{joke_id}"
        )

        st.success(
            response.json()["message"]
        )

# =========================================
# FILE UPLOAD
# =========================================

elif menu == "📤 Upload File":

    st.subheader("📤 Upload Meme/Image")

    uploaded_file = st.file_uploader(
        "Choose Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            use_container_width=True
        )

        if st.button("Upload 🚀"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }

            response = requests.post(
                f"{BASE_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                st.success(
                    "File Uploaded Successfully 🎉"
                )

            else:

                st.error(
                    "Upload failed"
                )
