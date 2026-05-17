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
# SIDEBAR MENU
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
        A full-stack FastAPI + Streamlit humour platform.
        </p>

        <ul>
            <li>Create jokes</li>
            <li>Generate AI jokes</li>
            <li>Search jokes</li>
            <li>Upload memes/images</li>
            <li>Update/Delete jokes</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# ADD JOKE
# =========================================

elif menu == "➕ Add Joke":

    st.markdown(
        """
        <div class='card'>
        <h1>➕ Add Joke</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    joke = st.text_area(
        "Enter your joke"
    )

    if st.button("Add Joke 😂"):

        response = requests.post(
            f"{BASE_URL}/jokes",
            json={
                "joke": joke
            }
        )

        st.success(
            "Joke Added Successfully 🎉"
        )

# =========================================
# GET ALL JOKES
# =========================================

elif menu == "😂 Get Jokes":

    st.markdown(
        """
        <div class='card'>
        <h1>😂 All Posted Jokes</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        response = requests.get(
            f"{BASE_URL}/jokes"
        )

        jokes = response.json()

        if len(jokes) == 0:

            st.warning(
                "No jokes available yet 😢"
            )

        else:

            st.success(
                f"{len(jokes)} jokes found 🎉"
            )

            for index, joke in enumerate(
                jokes,
                start=1
            ):

                joke_text = joke.get(
                    "joke",
                    "No joke text found"
                )

                joke_id = joke.get(
                    "id",
                    index
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

    except Exception as e:

        st.error(
            f"Error loading jokes: {e}"
        )
# =========================================
# RANDOM JOKE
# =========================================

elif menu == "🎲 Random Joke":

    st.markdown(
        """
        <div class='card'>
        <h1>🎲 Random Joke</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Generate Random Joke 😂"):

        response = requests.get(
            f"{BASE_URL}/random-joke"
        )

        data = response.json()

        if "joke" in data:

            st.markdown(
                f"""
                <div class='card'>
                <h2>🤣 Random Joke</h2>
                <p style='font-size:24px'>
                {data['joke']}
                </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.error(
                "No jokes found"
            )

# =========================================
# AI JOKE GENERATOR
# =========================================

elif menu == "🤖 AI Joke Generator":

    st.markdown(
        """
        <div class='card'>
        <h1>🤖 AI Joke Generator</h1>
        <p>Generate jokes using AI 😂</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Generate AI Joke 🚀"):

        with st.spinner(
            "AI is thinking 😂"
        ):

            try:

                response = requests.get(
                    f"{BASE_URL}/ai-joke"
                )

                data = response.json()

                st.markdown(
                    f"""
                    <div class='card'>
                    <h2>🤣 AI Generated Joke</h2>
                    <p style='font-size:24px'>
                    {data['ai_joke']}
                    </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# =========================================
# SEARCH JOKE
# =========================================

elif menu == "🔍 Search Joke":

    keyword = st.text_input(
        "Enter keyword"
    )

    if st.button("Search 🔍"):

        response = requests.get(
            f"{BASE_URL}/search?keyword={keyword}"
        )

        jokes = response.json()

        if jokes:

            for joke in jokes:

                st.markdown(
                    f"""
                    <div class='card'>
                    <h3>🤣 Search Result</h3>
                    <p style='font-size:20px'>
                    {joke['joke']}
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
# UPDATE JOKE
# =========================================

elif menu == "✏️ Update Joke":

    joke_id = st.number_input(
        "Enter Joke ID",
        min_value=1
    )

    updated_joke = st.text_area(
        "Updated Joke"
    )

    if st.button("Update Joke ✏️"):

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
# DELETE JOKE
# =========================================

elif menu == "🗑️ Delete Joke":

    joke_id = st.number_input(
        "Enter Joke ID to Delete",
        min_value=1
    )

    if st.button("Delete Joke 🗑️"):

        response = requests.delete(
            f"{BASE_URL}/jokes/{joke_id}"
        )

        st.success(
            response.json()["message"]
        )

# =========================================
# FILE UPLOAD + VIEW FILES
# =========================================

elif menu == "📤 Upload File":

    st.markdown(
        """
        <div class='card'>
        <h1>📤 Upload Meme/Image</h1>
        <p>
        Upload funny memes and instantly preview them 😂
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Selected Image Preview",
            use_container_width=True
        )

        if st.button("Upload 🚀"):

            try:

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

                data = response.json()

                st.success(
                    "✅ File Uploaded Successfully"
                )

                st.write(
                    "Uploaded File:",
                    data["filename"]
                )

                if "uploaded_images" not in st.session_state:

                    st.session_state.uploaded_images = []

                st.session_state.uploaded_images.append(
                    uploaded_file
                )

            except Exception as e:

                st.error(
                    f"Upload Failed: {e}"
                )

    st.markdown("---")

    st.subheader("🖼️ Uploaded Meme Gallery")

    if (
        "uploaded_images" in st.session_state
        and len(st.session_state.uploaded_images) > 0
    ):

        cols = st.columns(3)

        for index, image in enumerate(
            st.session_state.uploaded_images
        ):

            with cols[index % 3]:

                st.image(
                    image,
                    use_container_width=True
                )

                st.caption(image.name)

    else:

        st.info(
            "No uploaded images yet"
        )
