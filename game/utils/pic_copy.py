import os
import shutil
import filecmp

def copy_media_files():
    """ 复制文件到指定目录，跳过内容相同的文件，并在必要时创建目标目录 """
    source_dir = "media/cargames-unblocked.com/uploads"
    dest_dir = "cargames-unblocked.com/media/cargames-unblocked.com/uploads"
    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        print(source_path, dest_path)
        if os.path.isfile(source_path):
            if os.path.exists(dest_path) and filecmp.cmp(source_path, dest_path, shallow=False):
                print(dest_path+'已存在')
            else:
                shutil.copy2(source_path, dest_path)
