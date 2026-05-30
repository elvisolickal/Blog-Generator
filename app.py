import streamlit as st
import google.generativeai as genai

# -------------------------------
# Configure Gemini API
# -------------------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")


# -------------------------------
# Function to Generate Blog
# -------------------------------
def handle_response(input_text, no_words, blog_style):

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    # Create Gemini Model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    # Start Chat Session
    convo = model.start_chat(history=[])

    # Prompt for blog generation
    prompt = f"""
    Write a blog post on the topic "{input_text}" 
    in a style suitable for "{blog_style}" readers.

    Ensure the blog is approximately {no_words} words.

    Requirements:
    - Use a clear and engaging writing style
    - Include relevant examples and explanations
    - Make the content informative and easy to understand
    - Structure the blog properly with headings
    """

    convo.send_message(prompt)

    return convo.last.text


# -------------------------------
# Streamlit UI Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# App Title
st.title("🤖 AI Blog Generator")
st.write("Generate high-quality blogs instantly using Gemini AI")

# User Input
input_text = st.text_input("Enter Blog Topic")

# Two Columns
col1, col2 = st.columns(2)

with col1:
    no_words = st.number_input(
        "Number of Words",
        min_value=100,
        max_value=5000,
        value=500,
        step=100
    )

with col2:
    blog_style = st.selectbox(
        "Target Audience",
        (
            "Researchers",
            "Data Scientists",
            "Common People"
        )
    )

# Generate Button
submit = st.button("Generate Blog")


# -------------------------------
# Generate Output
# -------------------------------
if submit:

    if input_text.strip() == "":
        st.warning("Please enter a blog topic.")
    else:
        with st.spinner("Generating Blog..."):

            try:
                response = handle_response(
                    input_text,
                    no_words,
                    blog_style
                )

                st.subheader("Generated Blog")
                st.write(response)

            except Exception as e:
                st.error(f"Error: {str(e)}")