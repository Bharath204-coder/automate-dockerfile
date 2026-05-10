def generate_dockerignore(language: str) -> str:
    
    # Common ignores for all languages
    common = """# Git
.git
.gitignore

# Editor
.vscode
.idea
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment files
.env
.env.local
.env.*.local

# Logs
*.log
logs/
"""

    python_ignores = """
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
.venv/
venv/
env/
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
"""

    node_ignores = """
# Node.js
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
.npm
dist/
build/
.next/
.nuxt/
"""

    go_ignores = """
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
"""

    java_ignores = """
# Java
*.class
*.jar
*.war
*.ear
target/
build/
.gradle/
"""

    ruby_ignores = """
# Ruby
*.gem
.bundle/
vendor/bundle/
log/
tmp/
"""

    php_ignores = """
# PHP
vendor/
composer.lock
"""

    language_map = {
        "Python":  python_ignores,
        "Node.js": node_ignores,
        "Go":      go_ignores,
        "Java":    java_ignores,
        "Ruby":    ruby_ignores,
        "PHP":     php_ignores,
    }

    specific = language_map.get(language, "")
    
    return common + specific