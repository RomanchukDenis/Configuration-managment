import os
import subprocess
import sys
import yaml

def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def get_commits_from_repo(repo_path):
    log_format = "--pretty=format:%H;%P;%an;%ad"
    git_command = ["git", "-C", repo_path, "log", log_format, "--date=iso"]
    result = subprocess.run(git_command, capture_output=True, text=True, check=True)

    commits = {}
    for line in result.stdout.strip().split("\n"):
        parts = line.split(";", 3)
        if len(parts) >= 4:
            commit_hash, parents, author, date = parts
            commits[commit_hash] = {
                "parents": parents.split() if parents else [],
                "author": author,
                "date": date
            }
    return commits

def generate_mermaid_graph(commits, mermaid_file):
    with open(mermaid_file, "w", encoding="utf-8") as file:
        file.write("flowchart TB\n")
        for commit_hash, data in commits.items():
            label = f"{data['date']}\\n{data['author']}"
            file.write(f'    {commit_hash}["{label}"]\n')
            for parent in data["parents"]:
                file.write(f"    {parent} --> {commit_hash}\n")

def render_mermaid_to_image(mermaid_file, output_file):
    try:
        subprocess.run(["mmdc", "-i", mermaid_file, "-o", output_file], check=True)
        print(f"Изображение графа сохранено: {output_file}")
        if sys.platform.startswith("darwin"):  # macOS
            subprocess.run(["open", output_file])
        elif sys.platform.startswith("win"):  # Windows
            os.startfile(output_file)
        else:  # Linux
            subprocess.run(["xdg-open", output_file])
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации изображения: {e}", file=sys.stderr)

def main():
    if len(sys.argv) != 2:
        print("Использование: python git_mermaid_dep.py <путь_к_yaml>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    repo_path = config["repository_path"]
    mermaid_file = os.path.join(repo_path, "commit_dependencies.mmd")
    image_file = os.path.join(repo_path, "commit_dependencies.png")

    commits = get_commits_from_repo(repo_path)
    if not commits:
        print("Коммиты в репозитории не найдены.")
        return

    generate_mermaid_graph(commits, mermaid_file)
    render_mermaid_to_image(mermaid_file, image_file)

if __name__ == "__main__":
    main()
