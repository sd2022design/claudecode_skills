import os
import json
import re

def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # YAMLフロントマターを抽出 (name と description)
    metadata = {}
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip().strip('"').strip("'")
    
    # フロントマターがない場合のフォールバック（ファイルパスから取得）
    if 'name' not in metadata:
        metadata['name'] = os.path.basename(os.path.dirname(file_path))
    if 'description' not in metadata:
        metadata['description'] = "No description provided."
        
    metadata['path'] = file_path
    return metadata

def main():
    skills = []
    # リポジトリ内を再帰的に検索
    for root, dirs, files in os.walk('.'):
        if 'SKILL.md' in files:
            file_path = os.path.join(root, 'SKILL.md')
            # scriptsや.githubディレクトリは除外
            if not any(x in file_path for x in ['./scripts', './.github', './.git']):
                skills.append(extract_metadata(file_path))

    with open('skills.json', 'w', encoding='utf-8') as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
