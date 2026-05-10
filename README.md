# automate-dockerfile 🐳

Automatically generate production-ready Dockerfiles using Local LLMs (Ollama + CodeLlama) — no internet required, no API costs, 100% private.

## 📌 What it does
- Scans your project directory
- Detects language, framework, dependencies and port automatically
- Generates a production-ready Dockerfile
- Generates a .dockerignore file

## 🎥 Demo
<!-- Add your demo video/gif here -->

## 🏗️ Architecture
```
Your Project Folder
        ↓
Python Analyzer (detects language, framework, port, deps)
        ↓
Prompt Builder (builds smart prompt)
        ↓
Ollama + CodeLlama (local LLM)
        ↓
Dockerfile + .dockerignore
```
## 🌐 Supported Languages & Frameworks
| Language | Frameworks |
|----------|------------|
| Python   | FastAPI, Flask, Django |
| Node.js  | Express, Next.js, NestJS, Fastify |
| Go       | Standard library |
| Java     | Spring Boot |
| Ruby     | Rails |
| PHP      | Laravel, Symfony |

## ⚙️ Requirements
- Python 3.x
- Ollama installed and running
- CodeLlama model pulled

## 🚀 Installation

### 1. Clone the repo
```bash
git clone https://github.com/Bharath204-coder/automate-dockerfile
cd automate-dockerfile
```

### 2. Install dependencies
```bash
pip install requests
```

### 3. Install Ollama
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### 4. Pull CodeLlama model
```bash
ollama pull codellama
```

## 📖 Usage

### Start Ollama
```bash
ollama serve
```

### Generate Dockerfile
```bash
python3 main.py /path/to/your/project
```

### Example output
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s CMD curl -f http://localhost:8000 || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 How it works
1. **Analyzer** — scans project files, detects language, framework, dependencies and port
2. **Prompt Builder** — builds a detailed prompt with all project info
3. **LLM Client** — sends prompt to CodeLlama via Ollama API
4. **Output** — saves Dockerfile and .dockerignore to your project folder

## 📁 Project Structure
```
automate-dockerfile/
├── main.py                   # Entry point
├── analyzer.py               # Project scanner
├── prompt_builder.py         # Prompt generator
├── llm_client.py             # Ollama API client
├── dockerignore_generator.py # .dockerignore generator
└── README.md
```
## 🛠️ Built With
- Python 3.x
- Ollama
- CodeLlama
- AWS EC2

## 🤝 Contributing
Pull requests are welcome!

## 📄 License
MIT License

## 👨‍💻 Author
Bharath
