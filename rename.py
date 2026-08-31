import os
import shutil
import subprocess
from pathlib import Path

# 1. Rename directories
print("Moving java package...")

def move_package(src, dest):
    if os.path.exists(src):
        # ensure parent exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        # Move the entire directory
        shutil.move(src, dest)

move_package("app/src/main/java/com/kush/cachedeal", "app/src/main/java/com/kush/swych")
move_package("app/src/test/java/com/kush/cachedeal", "app/src/test/java/com/kush/swych")
move_package("app/src/androidTest/java/com/kush/cachedeal", "app/src/androidTest/java/com/kush/swych")

# 2. Text Replacements
print("Replacing text...")
replacements = {
    "com.kush.cachedeal": "com.kush.swych",
    "CacheDealTheme": "SwychTheme",
    "CacheDeal": "Swych",
    "cachedeal": "swych",
    "Cachedeal": "Swych"
}

exts = {".kt", ".xml", ".kts", ".md", ".json", ".properties", ".gradle"}
ignored_dirs = {".git", "build", ".gradle", ".idea"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ignored_dirs]
    for file in files:
        if Path(file).suffix in exts:
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            orig = content
            # Special case for strings.xml app name to ensure exact match
            if file == "strings.xml" and "app_name" in content:
                content = content.replace('>CacheDeal<', '>Swych<')
                
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filepath}")
