import re
import json
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
               "dist", "build", ".next"}

MANIFEST_MAP = {
    "package.json":     "Node.js",
    "requirements.txt": "Python",
    "pyproject.toml":   "Python",
    "go.mod":           "Go",
    "Cargo.toml":       "Rust",
    "pom.xml":          "Java",
    "build.gradle":     "Java",
    "Gemfile":          "Ruby",
    "composer.json":    "PHP",
}

ENTRY_POINTS = [
    "main.py", "app.py", "server.py",
    "index.js", "server.js", "app.js",
    "main.go", 
    "Main.java", "Application.java"
    "main.rs",
    "index.php",
    "app.rb", "config.ru"
]

#Analyze project
def analyze_project(project_path: str) -> dict:
    path = Path(project_path).resolve()
    files = [
        f for f in path.rglob("*")
        if f.is_file() and not any(p in f.parts for p in IGNORE_DIRS)
    ]
    print(f"  Found {len(files)} files")
    language = detect_language(path, files)
    deps = detect_dependencies(path, language)
    framework = detect_framework(path, language, deps)  # ← new!
    port = detect_port(path, files, framework)
    entry_point = None
    for candidate in ENTRY_POINTS:
        if (path / candidate).exists():
            entry_point = candidate
            break
    return {
        "language": language,
        "framework": framework,        # ← new!
        "dependencies": deps,
        "entry_point": entry_point,
        "port": port,
        "files": [f.name for f in files][:20],
    }

#Detect Language
def detect_language(path, files):
    file_names = {f.name for f in files}
    
    for manifest, lang in MANIFEST_MAP.items():
        if manifest in file_names:
            return lang
    
    return "Unknown"

#Detect Dependencies
def detect_dependencies(path, language):
    deps = []
    
    if language == "Python":
        req_file = path / "requirements.txt"
        if req_file.exists():
            lines = req_file.read_text().splitlines()
            deps = [l.strip().split("==")[0].split(">=")[0]
                    for l in lines if l.strip() and not l.startswith("#")]
    
    elif language == "Node.js":
        pkg_file = path / "package.json"
        if pkg_file.exists():
            pkg = json.loads(pkg_file.read_text())
            deps = list(pkg.get("dependencies", {}).keys())
    
    elif language == "Java":
        pom_file = path / "pom.xml"
        if pom_file.exists():
            deps = ["maven"]
    
    elif language == "Go":
        go_file = path / "go.mod"
        if go_file.exists():
            lines = go_file.read_text().splitlines()
            deps = [l.strip().split(" ")[0] 
                    for l in lines if l.startswith("\t") or l.startswith("require")]
    
    elif language == "Ruby":
        gemfile = path / "Gemfile"
        if gemfile.exists():
            lines = gemfile.read_text().splitlines()
            deps = [l.strip().split("'")[1] 
                    for l in lines if l.strip().startswith("gem '")]
    
    elif language == "PHP":
        composer_file = path / "composer.json"
        if composer_file.exists():
            composer = json.loads(composer_file.read_text())
            deps = list(composer.get("require", {}).keys())
    
    return deps


#Detect Framework
def detect_framework(path, language, deps):
    dep_str = " ".join(deps).lower()
    
    if language == "Python":
        if "django"  in dep_str: return "Django"
        if "fastapi" in dep_str: return "FastAPI"
        if "flask"   in dep_str: return "Flask"
        if "tornado" in dep_str: return "Tornado"
        if "aiohttp" in dep_str: return "aiohttp"
    
    elif language == "Node.js":
        if "express"  in dep_str: return "Express"
        if "next"     in dep_str: return "Next.js"
        if "nuxt"     in dep_str: return "Nuxt"
        if "fastify"  in dep_str: return "Fastify"
        if "nestjs"   in dep_str: return "NestJS"
    
    elif language == "Java":
        if (path / "pom.xml").exists():
            content = (path / "pom.xml").read_text().lower()
            if "spring-boot" in content: return "Spring Boot"
    
    elif language == "Ruby":
        if "rails" in dep_str: return "Rails"
    
    elif language == "PHP":
        if "laravel" in dep_str: return "Laravel"
        if "symfony" in dep_str: return "Symfony"
    
    return None
#Detect port
def detect_port(path, files, framework=None):
    
    # Method 1: Scan source files
    PORT_PATTERNS = [
        r'port\s*[=:]\s*(\d{4,5})',
        r'\.listen\(\s*(\d{4,5})',
        r'PORT\s*=\s*["\']?(\d{4,5})',
    ]
    
    source_files = [f for f in files if f.suffix in {".py", ".js", ".ts"}][:20]
    
    for f in source_files:
        try:
            content = f.read_text(errors="ignore")
            for pattern in PORT_PATTERNS:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        except Exception:
            continue

    # Method 2: Check .env file
    env_file = path / ".env"
    if env_file.exists():
        try:
            content = env_file.read_text()
            match = re.search(r'PORT\s*=\s*(\d{4,5})', content)
            if match:
                return int(match.group(1))
        except Exception:
            pass

    # Method 3: Framework default ports
    framework_ports = {
        "FastAPI":      8000,
        "Flask":        5000,
        "Django":       8000,
        "Express":      3000,
        "Next.js":      3000,
        "Spring Boot":  8080,
        "Rails":        3000,
        "PHP":          80,
    }

    if framework and framework in framework_ports:
        return framework_ports[framework]

    # Default
    return 8080
