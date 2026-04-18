# 🤖 AI BA Assistant: Document-to-Tasks

A specialized AI application designed for **Business Analysts (BA)**, **QA**, and **Service Engineers** to automate project workflows. This tool leverages Generative AI to transform static documents into actionable task breakdowns.

---

## 🌟 Overview

This project focuses on **Operational Optimization**. By utilizing Multimodal LLMs (GPT-4o-mini), the assistant reads complex documentation (Requirements, Meeting Minutes, or Financial Statements) and performs two core functions:

1. **Contextual Summarization**: Distills long documents into key project insights.
2. **Autonomous Task Breakdown**: Categorizes actions by role (Dev, QA, BA, Designer) and identifies priorities.

---

## 🛠️ Tech Stack

- **Language**: [Python 3.x](https://www.python.org/)
- **Interface**: [Streamlit](https://streamlit.io/) (Rapid UI development)
- **AI Engine**: [OpenAI API](https://openai.com/api/) (GPT-4o-mini)
- **Extraction**: `PyPDF2` for PDF parsing
- **Environment**: `python-dotenv` for secure API key management

---

## 🚀 Step-by-Step Setup Instructions

Follow these steps to get the environment running on your local machine:

### 1. Clone the Repository

```bash
git clone [https://github.com/thaotran1995/ai-ba-assistant.git](https://github.com/thaotran1995/ai-ba-assistant.git)
cd ai-ba-assistant
```

### Create the environment

```bash
python -m venv venv
```

### Activate it

#### Windows:

```bash
.\venv\Scripts\activate
```

#### Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration (.env)

Create a file named .env in the root directory.
Add your OpenAI API key (this file is ignored by Git for security)

### Launch the Application

```bash
streamlit run app.py
```
