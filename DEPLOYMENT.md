<<<<<<< HEAD
# 🚀 HƯỚNG DẪN DEPLOY HỆ THỐNG QUẢN LÝ PHIẾU KỸ THUẬT

## 📋 Yêu cầu hệ thống
- Python 3.9+
- Git
- Tài khoản trên platform deployment

---

## 🌐 PHƯƠNG ÁN 1: RENDER.COM (KHUYẾN NGHỊ)

### Bước 1: Chuẩn bị
1. Đăng ký tài khoản tại [render.com](https://render.com)
2. Kết nối GitHub repository

### Bước 2: Deploy
1. Vào Dashboard → New → Web Service
2. Chọn repository của bạn
3. Cấu hình:
   - **Name**: hai-tools-system
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_sqlite:app`
   - **Plan**: Free

### Bước 3: Environment Variables
Thêm các biến môi trường:
- `SECRET_KEY`: Tạo key ngẫu nhiên
- `PYTHON_VERSION`: 3.9.16

### Bước 4: Deploy
Click "Create Web Service" và chờ deploy hoàn tất.

---

## 🚄 PHƯƠNG ÁN 2: RAILWAY.APP

### Bước 1: Chuẩn bị
1. Đăng ký tại [railway.app](https://railway.app)
2. Kết nối GitHub

### Bước 2: Deploy
1. New Project → Deploy from GitHub repo
2. Chọn repository
3. Railway sẽ tự động detect Python và deploy

### Bước 3: Cấu hình
- Thêm environment variables nếu cần
- Railway tự động tạo URL

---

## ☁️ PHƯƠNG ÁN 3: HEROKU

### Bước 1: Cài đặt Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Hoặc tải từ https://devcenter.heroku.com/articles/heroku-cli
```

### Bước 2: Login và Deploy
```bash
heroku login
heroku create hai-tools-system
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Bước 3: Cấu hình Database
```bash
heroku addons:create heroku-postgresql:mini
```

---

## 🔧 PHƯƠNG ÁN 4: VPS/CLOUD SERVER

### Bước 1: Chuẩn bị VPS
- Ubuntu 20.04+ hoặc CentOS 8+
- Python 3.9+
- Nginx
- Gunicorn

### Bước 2: Cài đặt
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài Python và pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Tạo user cho app
sudo useradd -m -s /bin/bash hai-tools
sudo su - hai-tools

# Clone code
git clone <your-repo-url>
cd TOOLS-DEMO

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Test chạy
python app_sqlite.py
```

### Bước 3: Cấu hình Gunicorn
```bash
# Tạo service file
sudo nano /etc/systemd/system/hai-tools.service
```

Nội dung file:
```ini
[Unit]
Description=HAI Tools System
After=network.target

[Service]
User=hai-tools
WorkingDirectory=/home/hai-tools/TOOLS-DEMO
Environment="PATH=/home/hai-tools/TOOLS-DEMO/venv/bin"
ExecStart=/home/hai-tools/TOOLS-DEMO/venv/bin/gunicorn --workers 3 --bind unix:hai-tools.sock -m 007 app_sqlite:app

[Install]
WantedBy=multi-user.target
```

### Bước 4: Cấu hình Nginx
```bash
sudo nano /etc/nginx/sites-available/hai-tools
```

Nội dung:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/hai-tools/TOOLS-DEMO/hai-tools.sock;
    }
}
```

### Bước 5: Kích hoạt
```bash
sudo systemctl start hai-tools
sudo systemctl enable hai-tools
sudo ln -s /etc/nginx/sites-available/hai-tools /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

---

## 🔐 BẢO MẬT PRODUCTION

### 1. Environment Variables
```bash
export SECRET_KEY="your-super-secret-key-here"
export FLASK_ENV="production"
export DATABASE_URL="your-database-url"
```

### 2. HTTPS/SSL
- Sử dụng Let's Encrypt cho VPS
- Render/Railway tự động có HTTPS

### 3. Database
- Sử dụng PostgreSQL thay vì SQLite cho production
- Backup định kỳ

---

## 📊 MONITORING

### 1. Logs
```bash
# Xem logs
heroku logs --tail  # Heroku
railway logs        # Railway
sudo journalctl -u hai-tools -f  # VPS
```

### 2. Health Check
Tạo endpoint `/health` để kiểm tra trạng thái hệ thống.

---

## 🚨 TROUBLESHOOTING

### Lỗi thường gặp:
1. **Port binding**: Đảm bảo sử dụng `os.environ.get('PORT', 5000)`
2. **Database**: Kiểm tra quyền ghi file SQLite
3. **Dependencies**: Đảm bảo `requirements.txt` đầy đủ
4. **Static files**: Cấu hình đúng đường dẫn

### Debug:
```bash
# Kiểm tra logs
tail -f /var/log/nginx/error.log
sudo journalctl -u hai-tools -n 50
```

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, hãy kiểm tra:
1. Logs của platform
2. Cấu hình environment variables
3. Dependencies trong requirements.txt
4. Quyền truy cập file database

**Chúc bạn deploy thành công! 🎉**
=======
# 🚀 HƯỚNG DẪN DEPLOY HỆ THỐNG QUẢN LÝ PHIẾU KỸ THUẬT

## 📋 Yêu cầu hệ thống
- Python 3.9+
- Git
- Tài khoản trên platform deployment

---

## 🌐 PHƯƠNG ÁN 1: RENDER.COM (KHUYẾN NGHỊ)

### Bước 1: Chuẩn bị
1. Đăng ký tài khoản tại [render.com](https://render.com)
2. Kết nối GitHub repository

### Bước 2: Deploy
1. Vào Dashboard → New → Web Service
2. Chọn repository của bạn
3. Cấu hình:
   - **Name**: hai-tools-system
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_sqlite:app`
   - **Plan**: Free

### Bước 3: Environment Variables
Thêm các biến môi trường:
- `SECRET_KEY`: Tạo key ngẫu nhiên
- `PYTHON_VERSION`: 3.9.16

### Bước 4: Deploy
Click "Create Web Service" và chờ deploy hoàn tất.

---

## 🚄 PHƯƠNG ÁN 2: RAILWAY.APP

### Bước 1: Chuẩn bị
1. Đăng ký tại [railway.app](https://railway.app)
2. Kết nối GitHub

### Bước 2: Deploy
1. New Project → Deploy from GitHub repo
2. Chọn repository
3. Railway sẽ tự động detect Python và deploy

### Bước 3: Cấu hình
- Thêm environment variables nếu cần
- Railway tự động tạo URL

---

## ☁️ PHƯƠNG ÁN 3: HEROKU

### Bước 1: Cài đặt Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Hoặc tải từ https://devcenter.heroku.com/articles/heroku-cli
```

### Bước 2: Login và Deploy
```bash
heroku login
heroku create hai-tools-system
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Bước 3: Cấu hình Database
```bash
heroku addons:create heroku-postgresql:mini
```

---

## 🔧 PHƯƠNG ÁN 4: VPS/CLOUD SERVER

### Bước 1: Chuẩn bị VPS
- Ubuntu 20.04+ hoặc CentOS 8+
- Python 3.9+
- Nginx
- Gunicorn

### Bước 2: Cài đặt
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài Python và pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Tạo user cho app
sudo useradd -m -s /bin/bash hai-tools
sudo su - hai-tools

# Clone code
git clone <your-repo-url>
cd TOOLS-DEMO

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Test chạy
python app_sqlite.py
```

### Bước 3: Cấu hình Gunicorn
```bash
# Tạo service file
sudo nano /etc/systemd/system/hai-tools.service
```

Nội dung file:
```ini
[Unit]
Description=HAI Tools System
After=network.target

[Service]
User=hai-tools
WorkingDirectory=/home/hai-tools/TOOLS-DEMO
Environment="PATH=/home/hai-tools/TOOLS-DEMO/venv/bin"
ExecStart=/home/hai-tools/TOOLS-DEMO/venv/bin/gunicorn --workers 3 --bind unix:hai-tools.sock -m 007 app_sqlite:app

[Install]
WantedBy=multi-user.target
```

### Bước 4: Cấu hình Nginx
```bash
sudo nano /etc/nginx/sites-available/hai-tools
```

Nội dung:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/hai-tools/TOOLS-DEMO/hai-tools.sock;
    }
}
```

### Bước 5: Kích hoạt
```bash
sudo systemctl start hai-tools
sudo systemctl enable hai-tools
sudo ln -s /etc/nginx/sites-available/hai-tools /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

---

## 🔐 BẢO MẬT PRODUCTION

### 1. Environment Variables
```bash
export SECRET_KEY="your-super-secret-key-here"
export FLASK_ENV="production"
export DATABASE_URL="your-database-url"
```

### 2. HTTPS/SSL
- Sử dụng Let's Encrypt cho VPS
- Render/Railway tự động có HTTPS

### 3. Database
- Sử dụng PostgreSQL thay vì SQLite cho production
- Backup định kỳ

---

## 📊 MONITORING

### 1. Logs
```bash
# Xem logs
heroku logs --tail  # Heroku
railway logs        # Railway
sudo journalctl -u hai-tools -f  # VPS
```

### 2. Health Check
Tạo endpoint `/health` để kiểm tra trạng thái hệ thống.

---

## 🚨 TROUBLESHOOTING

### Lỗi thường gặp:
1. **Port binding**: Đảm bảo sử dụng `os.environ.get('PORT', 5000)`
2. **Database**: Kiểm tra quyền ghi file SQLite
3. **Dependencies**: Đảm bảo `requirements.txt` đầy đủ
4. **Static files**: Cấu hình đúng đường dẫn

### Debug:
```bash
# Kiểm tra logs
tail -f /var/log/nginx/error.log
sudo journalctl -u hai-tools -n 50
```

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, hãy kiểm tra:
1. Logs của platform
2. Cấu hình environment variables
3. Dependencies trong requirements.txt
4. Quyền truy cập file database

**Chúc bạn deploy thành công! 🎉**
>>>>>>> cad4acc09904766658dc682f1d2e0e72db707bbf
