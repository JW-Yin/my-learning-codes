import os
import re
from mutagen.flac import FLAC
from mutagen import MutagenError

def is_valid_flac(file_path):
    """验证文件是否为有效的FLAC文件"""
    try:
        FLAC(file_path)
        return True
    except MutagenError:
        return False

def extract_metadata_from_filename(filename):
    """从多种文件名格式中提取歌手和歌曲名"""
    # 格式1: 歌手《歌曲》[xxx].flac
    pattern1 = re.compile(r'^(.*?)《(.*?)》.*\.flac$', re.IGNORECASE)
    # 格式2: 歌曲名 - 歌手.flac
    pattern2 = re.compile(r'^(.*?) - (.*?)\.flac$', re.IGNORECASE)
    # 格式3: 纯歌曲名.flac
    pattern3 = re.compile(r'^(.*?)\.flac$', re.IGNORECASE)
    
    match = pattern1.match(filename)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    match = pattern2.match(filename)
    if match:
        return match.group(2).strip(), match.group(1).strip()
    
    match = pattern3.match(filename)
    if match:
        return "未知艺术家", match.group(1).strip()
    
    return None, None

def update_flac_metadata(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith('.flac'):
            continue
        
        file_path = os.path.join(folder_path, filename)
        
        # 先验证文件是否为有效FLAC
        if not is_valid_flac(file_path):
            print(f"❌ 无效FLAC文件: {filename}")
            continue
        
        # 提取歌手和歌曲名
        artist, title = extract_metadata_from_filename(filename)
        if not artist or not title:
            print(f"⚠️  无法解析: {filename}")
            continue
        
        # 写入元数据
        try:
            audio = FLAC(file_path)
            audio['artist'] = artist
            audio['title'] = title
            audio.save()
            print(f"✅ 已更新: {filename} → 歌手: {artist}, 标题: {title}")
        except Exception as e:
            print(f"❌ 写入失败: {filename} → 错误: {str(e)}")

if __name__ == "__main__":
    target_folder = r"D:\Public\music"  # 改成你的音乐文件夹路径
    update_flac_metadata(target_folder)