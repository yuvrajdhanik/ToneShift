# 📝 ToneShift

ToneShift is an AI-powered text rewriting application that rewrites text while preserving its original meaning.

Built with **Python**, **Streamlit**, and the **OpenRouter API**.

## Features

- ✨ Rewrite text without changing its meaning
- 📏 Adjustable rewrite length
- 🎭 Five standard writing tones
  - Child-Friendly
  - College Student
  - Casual
  - Professional
  - Executive
- 🤓 Nerd Mode
- 🪶 Shakespearean Mode
- 🔄 Back Translation
- 🔍 Semantic Similarity Analysis

## Installation

Clone the repository:

```bash
git clone https://github.com/yuvrajdhanik/ToneShift.git
cd ToneShift
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## Project Structure

```
ToneShift/
├── app.py
├── LICENSE
├── rewriter.py
├── prompts.py
├── requirements.txt
└── README.md
```

## Tech Stack

- Python
- Streamlit
- OpenRouter API
- OpenAI Python SDK

## License

This project is licensed under the MIT License.