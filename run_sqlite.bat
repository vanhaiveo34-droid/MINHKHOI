@echo off
echo ========================================
echo    Hệ thống Quản lý Phiếu Kỹ thuật
echo    (Phiên bản SQLite - Dễ dàng test)
echo ========================================
echo.

echo Đang kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Lỗi: Python chưa được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python 3.7+ và thử lại
    pause
    exit /b 1
)

echo Đang kiểm tra môi trường ảo...
if not exist "venv" (
    echo Tạo môi trường ảo...
    python -m venv venv
)

echo Kích hoạt môi trường ảo...
call venv\Scripts\activate.bat

echo Cài đặt dependencies...
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF WTForms python-dotenv Werkzeug email-validator

echo.
echo Khởi tạo dữ liệu mẫu...
python init_data.py

echo.
echo Khởi chạy ứng dụng (SQLite)...
echo Ứng dụng sẽ chạy tại: http://localhost:5000
echo Nhấn Ctrl+C để dừng
echo.
python app_sqlite.py

pause
