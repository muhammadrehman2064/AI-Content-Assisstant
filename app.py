import streamlit as st
from groq import Groq

# Set page layout
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts for social media platforms using Groq AI.")

# Retrieve API key securely from Streamlit secrets or user input
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not api_key:
    # Check if configured in Streamlit Secrets
    api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.info("💡 Please enter your Groq API key in the sidebar to continue.", icon="🔑")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Input Controls
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("Select Platform", ["LinkedIn", "Twitter/X", "Instagram", "Facebook"])
    content_type = st.selectbox("Content Type", ["Informational Post", "Storytelling", "Product Launch", "Opinion / Thought Leadership", "Call to Action"])

with col2:
    tone = st.selectbox("Select Tone", ["Professional", "Casual & Friendly", "Energetic & Hype", "Witty & Humorous", "Educational"])
    target_audience = st.text_input("Target Audience", placeholder="e.g. Software Engineers, Entrepreneurs")

topic = st.text_area("Topic or Core Message", placeholder="e.g. Benefits of microservices architecture in modern software engineering...")

# Generation Trigger
if st.button("🚀 Generate Content", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please provide a topic for your content.")
    else:
        with st.spinner("Drafting your post..."):
            prompt = f"""
            You are an expert social media content manager. Generate a high-converting post based on these requirements:

            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Topic: {topic}

            Output structure:
            1. **Post Content / Caption**: Optimized formatting (line breaks, emojis if appropriate) for {platform}.
            2. **Relevant Hashtags**: 3 to 7 high-performing hashtags tailored to the platform.
            """

            try:
                # Using Groq's fast Llama 3.1 8B model
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a creative social media content strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                generated_text = response.choices[0].message.content

                st.success("Generated Content:")
                st.markdown(generated_text)
                
                # Copy/Download convenience button
                st.download_button(
                    label="📥 Download Post as Text",
                    data=generated_text,
                    file_name=f"{platform.lower()}_post.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error generating content: {e}")
