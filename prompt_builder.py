def build_prompt(info: dict) -> str:
    lang  = info.get("language", "Unknown")
    framework = info.get("framework") or "None detected"
    deps  = info.get("dependencies", [])
    entry = info.get("entry_point") or "Not found"
    port  = info.get("port", 8080)
    files = info.get("files", [])

    dep_list = "\n".join(f"  - {d}" for d in deps) if deps else "  (none detected)"

    return f"""You are a senior DevOps engineer. Generate a production-ready Dockerfile.

PROJECT DETAILS:
Language    : {lang}
Framework   : {framework}
Entry point : {entry}
Port        : {port}

Dependencies:
{dep_list}

Files in project:
{chr(10).join("  - " + f for f in files)}

REQUIREMENTS:
1. Use official minimal base image (alpine or slim) for {lang}
2. Run as non-root user for security
3. Set WORKDIR to /app first
4. Then COPY dependency files and install them
5. Then COPY the rest of source code
6. EXPOSE the correct port {port}
7. Add a HEALTHCHECK
8. Add CMD to run the application correctly for {lang}

Language specific rules:
- Python/Django: CMD ["gunicorn", "wsgi:application"]
- Python/FastAPI: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
- Python/Flask: CMD ["python", "app.py"]
- Node.js/Express: CMD ["node", "index.js"]
- Node.js/Next.js: CMD ["npm", "run", "start"]
- Go: build binary first then run it
- Java/Spring Boot: CMD ["java", "-jar", "app.jar"]
- Ruby/Rails: CMD ["rails", "server", "-b", "0.0.0.0"]
- PHP/Laravel: CMD ["php", "artisan", "serve"]

The framework is {framework} - use it to generate the correct CMD!

Output ONLY the raw Dockerfile. No explanations, no markdown.
"""