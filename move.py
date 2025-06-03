import os
import shutil

# 定义源目录和目标目录
source_dir = 'nyt_crosswords'
target_dir = 'downloads'

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 遍历所有年份目录
for year in os.listdir(source_dir):
    year_path = os.path.join(source_dir, year)
    
    if not os.path.isdir(year_path):
        continue
    
    # 遍历所有月份目录
    for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)
        
        if not os.path.isdir(month_path):
            continue
        
        # 处理所有JSON文件
        for filename in os.listdir(month_path):
            if filename.endswith('.json'):
                file_path = os.path.join(month_path, filename)
                
                # 提取天数（移除.json扩展名）
                day = os.path.splitext(filename)[0]
                
                # 构建新文件名
                new_filename = f"{year}{month}{day}.json"
                target_path = os.path.join(target_dir, new_filename)
                
                # 移动并重命名文件
                shutil.move(file_path, target_path)
                print(f"Moved: {file_path} -> {target_path}")

print("所有文件移动完成！")