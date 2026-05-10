import sys
from pathlib import Path
from analyzer import analyze_project
from prompt_builder import build_prompt
from llm_client import generate_dockerfile_content
from dockerignore_generator import generate_dockerignore

def main():
    # Get project path from user
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("Enter project path: ").strip()

    print("\n[ 1/3 ] Analyzing project...")
    info = analyze_project(project_path)
    print(f"  Language   : {info['language']}")
    print(f"  Framework  : {info['framework']}")
    print(f"  Entry point: {info['entry_point']}")
    print(f"  Port       : {info['port']}")
    print(f"  Deps found : {len(info['dependencies'])}")

    print("\n[ 2/3 ] Building prompt...")
    prompt = build_prompt(info)
    print(f"  Prompt ready! ({len(prompt)} characters)")

    print("\n[ 3/3 ] Generating Dockerfile with Ollama...")
    dockerfile = generate_dockerfile_content(prompt)
    # Strip markdown fences if model added them
    if "```" in dockerfile:
        lines = dockerfile.splitlines()
        dockerfile = "\n".join(
            l for l in lines if not l.strip().startswith("```")
        ).strip()

    # Save the Dockerfile
    out_path = Path(project_path).resolve() / "Dockerfile"
    out_path.write_text(dockerfile)

    # Generate .dockerignore
    dockerignore = generate_dockerignore(info['language'])
    dockerignore_path = Path(project_path).resolve() / ".dockerignore"
    dockerignore_path.write_text(dockerignore)
    print(f"  .dockerignore saved to: {dockerignore_path}")

    print(f"\n  Dockerfile saved to: {out_path}")
    print("\n--- GENERATED DOCKERFILE ---")
    print(dockerfile)

if __name__ == "__main__":
    main()
