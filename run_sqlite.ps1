<<<<<<< HEAD
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Hệ thống Quản lý Phiếu Kỹ thuật" -ForegroundColor Yellow
Write-Host "   (Phiên bản SQLite - Dễ dàng test)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Đang kiểm tra Python..." -ForegroundColor Green
try {
    $pythonVersion = py --version
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Lỗi: Python chưa được cài đặt hoặc không có trong PATH" -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Python 3.7+ và thử lại" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host "Đang kiểm tra môi trường ảo..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    Write-Host "Tạo môi trường ảo..." -ForegroundColor Yellow
    py -m venv venv
}

Write-Host "Kích hoạt môi trường ảo..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

Write-Host "Cài đặt dependencies..." -ForegroundColor Green
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms python-dotenv Werkzeug email-validator

Write-Host ""
Write-Host "Khởi tạo dữ liệu mẫu..." -ForegroundColor Green
py init_data.py

Write-Host ""
Write-Host "Khởi chạy ứng dụng (SQLite)..." -ForegroundColor Green
Write-Host "Ứng dụng sẽ chạy tại: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Nhấn Ctrl+C để dừng" -ForegroundColor Yellow
Write-Host ""
py app_sqlite.py

Read-Host "Nhấn Enter để thoát"
=======
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Hệ thống Quản lý Phiếu Kỹ thuật" -ForegroundColor Yellow
Write-Host "   (Phiên bản SQLite - Dễ dàng test)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Đang kiểm tra Python..." -ForegroundColor Green
try {
    $pythonVersion = py --version
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Lỗi: Python chưa được cài đặt hoặc không có trong PATH" -ForegroundColor Red
    Write-Host "Vui lòng cài đặt Python 3.7+ và thử lại" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host "Đang kiểm tra môi trường ảo..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    Write-Host "Tạo môi trường ảo..." -ForegroundColor Yellow
    py -m venv venv
}

Write-Host "Kích hoạt môi trường ảo..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

Write-Host "Cài đặt dependencies..." -ForegroundColor Green
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms python-dotenv Werkzeug email-validator

Write-Host ""
Write-Host "Khởi tạo dữ liệu mẫu..." -ForegroundColor Green
py init_data.py

Write-Host ""
Write-Host "Khởi chạy ứng dụng (SQLite)..." -ForegroundColor Green
Write-Host "Ứng dụng sẽ chạy tại: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Nhấn Ctrl+C để dừng" -ForegroundColor Yellow
Write-Host ""
py app_sqlite.py

Read-Host "Nhấn Enter để thoát"
>>>>>>> cad4acc09904766658dc682f1d2e0e72db707bbf
