# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

st.title("AI Blog Generator")
st.write("Generate high-quality blog content with AI")

# Blog settings
topic = st.text_input("Blog Topic", "The Future of Technology")
word_count = st.slider("Approximate Word Count", 100, 1000, 500)

# Model selection
model = st.selectbox(
    "Select Model",
    [
        "meta-llama/Llama-2-7b-chat-hf",  # Requires approval but produces better content
        "tiiuae/falcon-7b-instruct",      # More capable model
        "togethercomputer/RedPajama-INCITE-7B-Instruct", # Decent for text generation
        "facebook/opt-2.7b",              # Larger OPT model
        "EleutherAI/gpt-j-6b"             # Larger model with better generation
    ]
)

# Better prompt templates
prompt_style = st.selectbox(
    "Content Style",
    ["Informative", "Creative", "Technical", "Persuasive"]
)

# Create a dictionary mapping style to prompt
prompt_templates = {
    "Informative": "Write a comprehensive blog post about {topic}. The blog should be informative, engaging, and well-structured with an introduction, main points, and conclusion. It should be approximately {word_count} words and avoid repetition.",
    "Creative": "Write a creative and engaging blog post about {topic}. Use vivid language, interesting analogies, and a conversational tone. Include a catchy introduction, 3-5 main sections, and a thoughtful conclusion. The blog should be about {word_count} words.",
    "Technical": "Write an in-depth technical blog post about {topic}. Include factual information, current trends, technical details, and practical applications. Structure it with an introduction, technical sections, practical implications, and a conclusion. The blog should be approximately {word_count} words.",
    "Persuasive": "Write a persuasive blog post about {topic}. Present a clear argument, supporting evidence, and address potential counterpoints. Use a confident tone and end with a strong call to action. The blog should be about {word_count} words."
}

if st.button("Generate Blog"):
    if not HUGGING_FACE_API_KEY:
        st.error("API key not found. Please set the HUGGING_FACE_API_KEY environment variable.")
    else:
        try:
            # Show progress
            with st.spinner("Generating blog content (this may take 30-60 seconds)..."):
                # API request to Hugging Face
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
                
                # Prepare prompt
                selected_prompt = prompt_templates[prompt_style].format(topic=topic, word_count=word_count)
                
                # Make API call with improved parameters
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={
                        "inputs": selected_prompt,
                        "parameters": {
                            "max_new_tokens": min(word_count * 6, 2048),
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "do_sample": True,
                            "repetition_penalty": 1.2
                        }
                    }
                )
                
                # Process response
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0], dict) and "generated_text" in result[0]:
                            blog_content = result[0]["generated_text"]
                        else:
                            blog_content = str(result[0])
                    elif isinstance(result, dict) and "generated_text" in result:
                        blog_content = result["generated_text"]
                    else:
                        blog_content = str(result)
                    
                    # Remove the prompt from the output if present
                    if selected_prompt in blog_content:
                        blog_content = blog_content.replace(selected_prompt, "")
                    
                    # Display the generated blog
                    st.subheader("Generated Blog")
                    st.write(blog_content)
                    
                    # Download option
                    st.download_button(
                        "Download Blog",
                        blog_content,
                        file_name=f"{topic.replace(' ', '_')}_blog.txt"
                    )
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"Details: {response.text}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")