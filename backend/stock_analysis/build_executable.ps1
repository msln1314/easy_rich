Write-Output "========================================"
Write-Output "Stock Analysis Tool Build Script"
Write-Output "========================================"
Write-Output ""

# Check PyInstaller
try {
    python -c "import pyinstaller" 2>$null
    Write-Output "PyInstaller is installed."
} catch {
    Write-Output "Installing PyInstaller..."
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Output "Failed to install PyInstaller. Please check your network."
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Output ""
Write-Output "Starting compilation of stock_analyze.py..."
Write-Output ""

# Compile
pyinstaller stock_analyze.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Output ""
    Write-Output "Compilation failed!"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Output ""
Write-Output "========================================"
Write-Output "Compilation Successful!"
Write-Output "========================================"
Write-Output ""
Write-Output "Executable is located at: dist\stock_analyze\stock_analyze.exe"
Write-Output ""
Write-Output "Usage:"
Write-Output "stock_analyze.exe -k 10 -d 30"
Write-Output "stock_analyze.exe -c 600519,000858"
Write-Output "stock_analyze.exe --help"
Write-Output ""
Read-Host "Press Enter to exit"
