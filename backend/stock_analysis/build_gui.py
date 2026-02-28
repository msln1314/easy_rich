import os
import shutil
import PyInstaller.__main__

def build():
    print("Starting build process for StockAnalyzeGUI...")
    
    # Run PyInstaller with the spec file
    PyInstaller.__main__.run([
        'stock_analyze_gui.spec',
        '--clean',
        '--noconfirm'
    ])
    
    print("Build complete.")
    
    # Check if dist/StockAnalyzeGUI.exe exists
    exe_path = os.path.join('dist', 'StockAnalyzeGUI.exe')
    if os.path.exists(exe_path):
        print(f"Executable created at: {os.path.abspath(exe_path)}")
        
        # Copy config.example.toml to dist folder for convenience
        if os.path.exists('config.example.toml'):
            shutil.copy('config.example.toml', os.path.join('dist', 'config.example.toml'))
            print("Copied config.example.toml to dist folder.")
            
        print("\nNOTE: Please ensure 'config.toml' is present in the same directory as the executable.")
        print("You can copy 'config.example.toml' to 'config.toml' and edit it.")
    else:
        print("Error: Executable not found in dist folder.")

if __name__ == "__main__":
    build()
