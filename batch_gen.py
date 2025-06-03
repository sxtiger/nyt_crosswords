import os
import json
from tqdm import tqdm
from gen import generate_puzzle_pdf, generate_solution_pdf

def batch_generate_from_folder(folder="downloads"):
    for filename in tqdm(sorted(os.listdir(folder)), desc="生成PDF"):
    # for filename in os.listdir(folder):
        if filename.endswith(".json"):
            json_path = os.path.join(folder, filename)
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                generate_puzzle_pdf(json_path, data)
                generate_solution_pdf(json_path, data)
            except Exception as e:
                print(f"❌ 处理文件 {filename} 时出错：{e}")

if __name__ == "__main__":
    batch_generate_from_folder()
