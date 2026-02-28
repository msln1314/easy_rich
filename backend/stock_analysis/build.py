"""Build script for creating executable using PyInstaller."""
import os
import sys
import shutil
from pathlib import Path
import traceback
import site

def clean_build_dirs():
    """Clean build and dist directories."""
    print("清理旧的构建文件...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def get_mini_racer_files():
    """Get py_mini_racer dependency files."""
    mini_racer_files = []
    for site_dir in site.getsitepackages():
        mini_racer_dir = os.path.join(site_dir, 'py_mini_racer')
        if os.path.exists(mini_racer_dir):
            for file in os.listdir(mini_racer_dir):
                if file.endswith(('.dll', '.dat', '.bin')):
                    src = os.path.join(mini_racer_dir, file)
                    mini_racer_files.append((src, '.'))
    return mini_racer_files

def get_akshare_files():
    """Get akshare data files."""
    akshare_files = []
    for site_dir in site.getsitepackages():
        akshare_dir = os.path.join(site_dir, 'akshare')
        if os.path.exists(akshare_dir):
            file_fold = os.path.join(akshare_dir, 'file_fold')
            if os.path.exists(file_fold):
                akshare_files.append((file_fold, 'akshare/file_fold'))
    return akshare_files

def build():
    """Build the executable."""
    try:
        clean_build_dirs()
        
        print("\n开始构建可执行文件...")
        
        # 获取依赖文件
        mini_racer_files = get_mini_racer_files()
        akshare_files = get_akshare_files()
        
        # 使用PyInstaller构建
        import PyInstaller.__main__
        args = [
            'stock_analysis.py',
            '--name=stock_analysis',
            '--onefile',
            '--console',
            '--add-data=version.py;.',
            '--hidden-import=akshare',
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=mplfinance',
            '--hidden-import=matplotlib',
            '--hidden-import=seaborn',
            '--hidden-import=tqdm',
            '--hidden-import=py_mini_racer',
            '--clean',
            '--noconfirm'
        ]
        
        # 添加依赖文件
        for src, dst in mini_racer_files:
            args.append(f'--add-binary={src};{dst}')
        
        for src, dst in akshare_files:
            args.append(f'--add-data={src};{dst}')
        
        PyInstaller.__main__.run(args)
        
        print("\n构建成功！")
        print("可执行文件位于: dist/stock_analysis.exe")
        
    except Exception as e:
        print("\n构建过程中出现错误:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print("\n详细错误信息:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    build()
