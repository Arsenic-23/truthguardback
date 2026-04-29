<div align="center">
  <h1>🛡️ TruthGuard Backend</h1>
  <p><strong>A lightning-fast, AI-powered fact-checking API built with FastAPI.</strong></p>
</div>

<br />

The **TruthGuard Backend** is the core processing engine for the TruthGuard platform. It leverages advanced NLP, OpenAI's GPT-4o-mini, and real-time web search (SerpAPI) to instantly verify claims, extract text from PDFs, and analyze web URLs for authenticity.

## ✨ Features

- ⚡️ **High-Performance API**: Built on [FastAPI](https://fastapi.tiangolo.com/) for incredibly fast, asynchronous request handling.
- 🤖 **LLM Integration**: Uses OpenAI's GPT-4o-mini for intelligent context evaluation and claim verification.
- 🌐 **Real-time Web Search**: Integrates with SerpAPI to fetch live web sources and cross-reference claims against current data.
- 📄 **Multi-format Support**: Process direct text input, scrape content from URLs, or extract text directly from PDF documents.
- 📊 **Scoring Engine**: Returns an actionable authenticity score along with cited sources and verification details.

## 🛠️ Tech Stack

- **Framework**: Python, FastAPI
- **Server**: Uvicorn
- **AI/LLM**: OpenAI API (`gpt-4o-mini`)
- **Search Integration**: SerpAPI (`httpx` for async fetching)
- **Document Processing**: PyPDF2
- **Environment**: `python-dotenv`

## 📂 Project Structure

```text
truthguardback-main-2/
├── app/
│   ├── main.py             # FastAPI application instance & CORS setup
│   ├── schemas.py          # Pydantic models for request validation
│   ├── routers/            # API Endpoints
│   │   ├── text.py         # POST /check-text
│   │   ├── url.py          # POST /check-url
│   │   └── pdf.py          # POST /check-pdf
│   └── services/           # Core Logic & Integrations
│       ├── checker.py      # Main evaluation pipeline
│       ├── extractor.py    # Text extraction utilities
│       ├── llm.py          # OpenAI API integration
│       ├── nlp.py          # Text preprocessing
│       ├── scoring.py      # Truth scoring algorithm
│       └── search.py       # SerpAPI web search integration
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables (git-ignored)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An [OpenAI API Key](https://platform.openai.com/)
- A [SerpAPI Key](https://serpapi.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/truthguard-backend.git
   cd truthguard-backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   ```

### Running the Server

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. 
You can view the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## 📡 API Endpoints

- `GET /` - Health check.
- `POST /check-text` - Submit raw text for verification.
- `POST /check-url` - Submit a URL to be scraped and verified.
- `POST /check-pdf` - Upload a PDF document for text extraction and verification.

All check endpoints return a structured JSON response containing an authenticity `score`, a list of `sources`, execution `duration_ms`, and evaluation `details`.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is licensed under the MIT License.
