# MCP Multi-Service Agent

A modular agent system that integrates multiple services (web search, weather, and research papers) using MCP (Model Control Protocol). Built with LangChain and powered by Groq's LLM capabilities.

## 🌟 Features

- **Web Search**: Search the web for up-to-date information
- **Weather**: Get current weather data for any location
- **Research Papers**: Find academic papers on various topics
- **Modular Architecture**: Each service runs as a separate MCP server
- **Interactive CLI**: User-friendly command-line interface
- **Asynchronous Processing**: Efficient handling of concurrent requests

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- API Keys (Groq, OpenWeatherMap)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
     ```

## 🛠️ Running the Application

1. **Start the services** (in separate terminal windows):

   ```bash
   # Terminal 1 - Weather Service
   python MCPSERVERLangchain/weather.py

   # Terminal 2 - Web Search Service
   python MCPSERVERLangchain/websearch_server.py

   # Terminal 3 - Research Papers Service
   python MCPSERVERLangchain/papers_server.py
   ```

2. **Run the client**
   ```bash
   python MCPSERVERLangchain/client.py
   ```

3. **Interact with the agent**
   - Type your query at the prompt
   - Example: "What's the weather in London?"
   - Type 'exit' to quit

## 🏗️ Project Structure

```
.
├── .env                    # Environment variables (not versioned)
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── client.py               # Main client application
├── papers_server.py        # Research papers service
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Project dependencies
├── uv.lock                # UV package manager lock file
├── weather.py             # Weather service
└── websearch_server.py    # Web search service

# Virtual Environment (not versioned)
.venv/                    # Python virtual environment
```

## 🤖 Available Tools

- **Web Search**: Get information from the web
  - Example: "Search for latest AI news"
  
- **Weather**: Get current weather information
  - Example: "What's the weather in Tokyo?"
  
- **Research Papers**: Find academic papers
  - Example: "Find papers about quantum computing"

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [Groq](https://groq.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [DuckDuckGo](https://duckduckgo.com/)
- [ArXiv](https://arxiv.org/)
