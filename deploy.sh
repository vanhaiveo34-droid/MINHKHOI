#!/bin/bash

# Script deploy tự động cho HAI Tools System
# Sử dụng cho VPS Ubuntu/CentOS

echo "🚀 Bắt đầu deploy HAI Tools System..."

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Vui lòng chạy script với quyền sudo"
    exit 1
fi

# Cập nhật hệ thống
echo "📦 Cập nhật hệ thống..."
apt update && apt upgrade -y

# Cài đặt dependencies
echo "🔧 Cài đặt dependencies..."
apt install python3 python3-pip python3-venv nginx git curl -y

# Tạo user cho app
echo "👤 Tạo user hai-tools..."
useradd -m -s /bin/bash hai-tools 2>/dev/null || echo "User hai-tools đã tồn tại"

# Chuyển sang user hai-tools
echo "📁 Thiết lập thư mục làm việc..."
su - hai-tools << 'EOF'

# Clone hoặc cập nhật code
if [ -d "TOOLS-DEMO" ]; then
    cd TOOLS-DEMO
    git pull origin main
else
    git clone https://github.com/your-username/TOOLS-DEMO.git
    cd TOOLS-DEMO
fi

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Tạo database nếu chưa có
python3 -c "
from app_sqlite import app, db
with app.app_context():
    db.create_all()
    print('Database đã được tạo!')
"

echo "✅ Cài đặt hoàn tất!"
EOF

# Tạo service file
echo "⚙️ Tạo systemd service..."
cat > /etc/systemd/system/hai-tools.service << 'EOF'
[Unit]
Description=HAI Tools System
After=network.target

[Service]
User=hai-tools
WorkingDirectory=/home/hai-tools/TOOLS-DEMO
Environment="PATH=/home/hai-tools/TOOLS-DEMO/venv/bin"
ExecStart=/home/hai-tools/TOOLS-DEMO/venv/bin/gunicorn --workers 3 --bind unix:/home/hai-tools/TOOLS-DEMO/hai-tools.sock -m 007 app_sqlite:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Tạo cấu hình Nginx
echo "🌐 Cấu hình Nginx..."
cat > /etc/nginx/sites-available/hai-tools << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/hai-tools/TOOLS-DEMO/hai-tools.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/hai-tools/TOOLS-DEMO/static;
    }
}
EOF

# Kích hoạt site
ln -sf /etc/nginx/sites-available/hai-tools /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Khởi động services
echo "🚀 Khởi động services..."
systemctl daemon-reload
systemctl enable hai-tools
systemctl start hai-tools
systemctl restart nginx

# Kiểm tra trạng thái
echo "📊 Kiểm tra trạng thái..."
systemctl status hai-tools --no-pager
systemctl status nginx --no-pager

# Hiển thị thông tin
echo ""
echo "🎉 DEPLOY THÀNH CÔNG!"
echo "📱 Truy cập: http://$(curl -s ifconfig.me)"
echo "📁 Logs: sudo journalctl -u hai-tools -f"
echo "🔄 Restart: sudo systemctl restart hai-tools"
echo "🛑 Stop: sudo systemctl stop hai-tools"
echo ""
echo "🔐 Mật khẩu mặc định:"
echo "   Quản trị viên: quan_tri_vien / quan_tri_vien123"
echo "   Quản lý: quan_ly1 / quan_ly123"
echo "   Kinh doanh: kinh_doanh1 / kinh_doanh123"
echo "   Kỹ thuật: ky_thuat1 / ky_thuat123"
