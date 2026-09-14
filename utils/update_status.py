import re
import subprocess
from pathlib import Path


def get_latest_lab_tag(lab_name: str) -> str | None:
    result = subprocess.run(
        [
            "git",
            "tag",
            "-l",
            f"submit/{lab_name}*",
            "--sort=-v:refname"
        ],
        capture_output=True,
        text=True,
        check=True
    )
    tags = [tag for tag in result.stdout.split('\n') if tag.strip()]
    
    if tags:
        return tags[0]
    return None

def update_status() -> None:
    readme_path = Path("README.md")
    labs_path = Path("labs")

    labs_subdirectories = sorted([path for path in labs_path.iterdir() if path.is_dir()])

    if not (readme_path.exists() and labs_path.exists()):
        raise FileNotFoundError(f"{readme_path.absolute()}, {labs_path.absolute()}")

    content = readme_path.read_text(encoding="utf-8")

    status_lines = []
    for lab_dir in labs_subdirectories:
        lab_name = lab_dir.name
        latest_tag = get_latest_lab_tag(lab_name)
        
        if latest_tag:
            status_lines.append(f"- [x] {lab_name} *(Completed: `{latest_tag}`)*")
        else:
            status_lines.append(f"- [ ] {lab_name}")

    text_to_replace_with = "\n".join(status_lines)

    pattern = r"(<!-- Status Start -->)(.*?)(<!-- Status End -->)"
    replacement = f"\\1\n{text_to_replace_with}\n\\3"

    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    readme_path.write_text(updated_content, encoding="utf-8")


if __name__ == "__main__":
    update_status()
