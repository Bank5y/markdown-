import os
import re
import requests
import logging
from tqdm import tqdm

# 配置日志记录
logging.basicConfig(filename='run.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def download_with_progress(url, filename, description):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=description)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def process_md_file(md_file, finished_files):
    # 检查是否已标记过或已处理过
    if md_file in finished_files or md_file.endswith('-本地副本.md'):
        logging.info(f"文件已标记过或已处理过: {md_file}")
        return

    logging.info(f"开始处理文件: {md_file}")

    # 创建同名文件夹
    folder_name = os.path.splitext(md_file)[0]
    os.makedirs(folder_name, exist_ok=True)
    img_folder = os.path.join(folder_name, 'img')
    mp3_folder = os.path.join(folder_name, 'mp3')
    os.makedirs(img_folder, exist_ok=True)
    os.makedirs(mp3_folder, exist_ok=True)

    # 读取.md文件内容
    with open(md_file, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # 匹配音频和图片标签
    audio_pattern = r'<audio[^>]*src="([^"]+)"[^>]*>'
    img_pattern = r'<img[^>]*src="([^"]+)"[^>]*>'

    # 下载音频资源
    audio_matches = re.findall(audio_pattern, md_content)
    for idx, audio_url in enumerate(audio_matches):
        audio_filename = os.path.join(mp3_folder, f'{os.path.basename(folder_name)}.mp3')
        try:
            download_with_progress(audio_url, audio_filename, f'{md_file} - mp3下载中...')
        except Exception as e:
            logging.error(f"下载音频文件失败: {audio_url}, 错误信息: {e}")
            continue
        md_content = md_content.replace(audio_url, f'../{audio_filename}')

    # 下载图片资源
    img_matches = re.findall(img_pattern, md_content)
    for idx, img_url in enumerate(img_matches):
        img_filename = os.path.join(img_folder, f'{os.path.basename(folder_name)}-img_{idx}.png')
        try:
            download_with_progress(img_url, img_filename, f'{md_file} - img{idx}下载中...')
        except Exception as e:
            logging.error(f"下载图片文件失败: {img_url}, 错误信息: {e}")
            continue
        md_content = md_content.replace(img_url, f'../{img_filename}')

    # 创建替换后的.md副本
    new_md_file = os.path.join(folder_name, f'{os.path.basename(folder_name)}-本地副本.md')
    with open(new_md_file, 'w', encoding='utf-8') as file:
        file.write(md_content)

    # 将文件名加入已处理列表中
    finished_files.add(md_file)
    with open('finish.txt', 'a', encoding='utf-8') as finish_file:
        finish_file.write(f"{md_file}\n")

    logging.info(f"文件处理完成: {md_file}")

if __name__ == "__main__":
    # 获取当前目录下的.md文件并依次处理
    scan_option = 'root'  # 设置扫描选项，可选值为 'root' 或 'sub'
    if scan_option == 'root':
        md_files = [filename for filename in os.listdir() if filename.endswith('.md')]
    elif scan_option == 'sub':
        md_files = []
        for root, dirs, files in os.walk('.'):
            # 只处理一级子目录下的文件
            if root == '.':
                md_files.extend([filename for filename in files if filename.endswith('.md')])
                continue
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))

    # 读取已处理文件列表
    finished_files = set()
    if os.path.exists('finish.txt'):
        with open('finish.txt', 'r', encoding='utf-8') as finish_file:
            finished_files = set(finish_file.read().splitlines())

    for md_file in md_files:
        process_md_file(md_file, finished_files)
