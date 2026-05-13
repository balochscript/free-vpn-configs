import json
import os
from datetime import datetime

def get_recent_configs(configs: list, limit: int = 100) -> list:
    return configs[:limit]

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(current_dir, '..', 'raw_configs.json')
    
    print("📋 Extracting recent configs...")
    
    with open(raw_path) as f:
        all_configs = json.load(f)
    
    recent = get_recent_configs(all_configs, 100)
    
    output_path = os.path.join(current_dir, '..', 'recent_configs.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(recent, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(recent)} recent configs")

if __name__ == '__main__':
    main()
