import os
import shutil
import argparse

def export_wallpaper(output_directory=None, image_path=None):
    """
    将指定的壁纸文件复制到输出目录，并以数字编号重命名
    
    参数:
    output_directory: 输出目录路径
    image_path: 源壁纸文件路径
    """
    
    # 设置默认路径
    if output_directory is None:
        output_directory = r"D:\wallpaper"
    if image_path is None:
        image_path = r"C:\Users\Jwyin\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
    
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"创建输出目录: {output_directory}")
    
    # 检查源文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 源文件不存在 - {image_path}")
        return None
    
    # 找出所有已存在的编号文件
    existing_files = []
    for file in os.listdir(output_directory):
        if file.endswith('.png'):
            # 提取文件名中的数字部分
            try:
                # 假设文件名格式为 "数字.png"
                num = int(os.path.splitext(file)[0])
                existing_files.append(num)
            except ValueError:
                # 如果文件名不是数字，跳过
                continue
    
    # 找到最小的未使用编号
    i = 0
    while i in existing_files:
        i += 1
    
    # 构建目标文件路径
    dest_path = os.path.join(output_directory, f"{i}.png")
    
    try:
        # 复制文件
        shutil.copy2(image_path, dest_path)
        print(f"成功复制壁纸到: {dest_path}")
        return dest_path
    except Exception as e:
        print(f"复制文件时出错: {e}")
        return None


if __name__ == "__main__":
    # 使用命令行参数
    parser = argparse.ArgumentParser(description='导出Windows壁纸')
    parser.add_argument('--output', '-o', 
                        default=r"D:\wallpaper",
                        help='输出目录路径')
    parser.add_argument('--source', '-s',
                        default=r"C:\Users\Jwyin\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper",
                        help='源壁纸文件路径')
    
    args = parser.parse_args()
    
    export_wallpaper(args.output, args.source)
