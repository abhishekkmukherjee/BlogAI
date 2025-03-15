# AI Blog Generator

A Streamlit web application that generates blog content using Hugging Face's AI models.

## Features

- Generate blog posts on any topic
- Customize word count and content style
- Choose from different AI models
- Download generated content as text files

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-blog-generator.git
   cd ai-blog-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Hugging Face API key:
   ```
   HUGGING_FACE_API_KEY=your_api_key_here
   ```

## Usage

Run the Streamlit app:
```
streamlit run app.py
```

The application will open in your default web browser. From there:

1. Enter your blog topic
2. Select desired word count
3. Choose a content style and model
4. Click "Generate Blog"

## Deployment

This app can be deployed on various platforms:

### Streamlit Cloud

1. Push your code to GitHub (make sure the `.env` file is in your `.gitignore`)
2. Deploy on [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your API key in the Streamlit Cloud secrets management

### Heroku

1. Create a Heroku app
2. Set environment variables in Heroku settings
3. Deploy from GitHub

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.streamlit run app.py