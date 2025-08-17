# 🚀 HƯỚNG DẪN PUSH CODE LÊN GITHUB

## 📋 **PHƯƠNG ÁN 1: SỬ DỤNG SCRIPT TỰ ĐỘNG (KHUYẾN NGHỊ)**

### Bước 1: Chạy script tự động
```powershell
# Mở PowerShell với quyền Administrator
# Chạy script tự động
.\setup_git_and_push.ps1
```

Script sẽ tự động:
- ✅ Cài đặt Git (nếu chưa có)
- ✅ Cấu hình Git với thông tin của bạn
- ✅ Khởi tạo repository (nếu chưa có)
- ✅ Commit và push code lên GitHub

---

## 📋 **PHƯƠNG ÁN 2: LÀM THỦ CÔNG**

### Bước 1: Cài đặt Git
1. Truy cập: https://git-scm.com/download/win
2. Tải và cài đặt Git cho Windows
3. Khởi động lại PowerShell

### Bước 2: Cấu hình Git
```powershell
# Cấu hình tên và email
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

### Bước 3: Khởi tạo repository (nếu chưa có)
```powershell
# Kiểm tra xem đã có .git chưa
ls -la

# Nếu chưa có .git, khởi tạo repository
git init
```

### Bước 4: Thêm file vào Git
```powershell
# Thêm tất cả file
git add .

# Kiểm tra trạng thái
git status
```

### Bước 5: Commit thay đổi
```powershell
git commit -m "Fix admin_users endpoint and add user management features"
```

### Bước 6: Tạo repository trên GitHub
1. Truy cập: https://github.com
2. Đăng nhập tài khoản
3. Click "New repository"
4. Đặt tên: `TOOLS-DEMO`
5. Chọn "Public" hoặc "Private"
6. **KHÔNG** chọn "Initialize this repository with a README"
7. Click "Create repository"

### Bước 7: Kết nối với GitHub
```powershell
# Thêm remote origin (thay thế URL bằng URL thực của bạn)
git remote add origin https://github.com/username/TOOLS-DEMO.git

# Kiểm tra remote
git remote -v
```

### Bước 8: Push code lên GitHub
```powershell
# Push lần đầu
git push -u origin main

# Nếu branch là master thay vì main
git push -u origin master
```

---

## 🔐 **XÁC THỰC GITHUB**

### Nếu được yêu cầu đăng nhập:
1. **Personal Access Token** (Khuyến nghị):
   - Vào GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token → Classic
   - Chọn quyền: `repo`, `workflow`
   - Copy token và sử dụng làm mật khẩu

2. **GitHub CLI**:
   ```powershell
   # Cài đặt GitHub CLI
   winget install --id GitHub.cli
   
   # Đăng nhập
   gh auth login
   ```

---

## ✅ **KIỂM TRA KẾT QUẢ**

### Sau khi push thành công:
1. Truy cập repository trên GitHub
2. Kiểm tra các file đã được upload
3. Vào Render dashboard
4. Kiểm tra logs để xem quá trình deploy

### Các file quan trọng cần có:
- ✅ `app_sqlite.py` (đã sửa lỗi admin_users)
- ✅ `templates/admin_users.html` (template mới)
- ✅ `init_production.py` (script khởi tạo dữ liệu)
- ✅ `render.yaml` (cấu hình Render)
- ✅ `requirements.txt` (dependencies)

---

## 🚨 **XỬ LÝ LỖI THƯỜNG GẶP**

### Lỗi 1: "git is not recognized"
```powershell
# Cài đặt Git từ: https://git-scm.com/download/win
# Hoặc sử dụng script tự động
.\setup_git_and_push.ps1
```

### Lỗi 2: "Authentication failed"
```powershell
# Tạo Personal Access Token trên GitHub
# Sử dụng token làm mật khẩu
```

### Lỗi 3: "Repository not found"
```powershell
# Kiểm tra URL repository
git remote -v

# Sửa URL nếu cần
git remote set-url origin https://github.com/username/TOOLS-DEMO.git
```

### Lỗi 4: "Permission denied"
```powershell
# Kiểm tra quyền truy cập repository
# Đảm bảo repository là public hoặc bạn có quyền push
```

---

## 🎯 **KẾT QUẢ MONG ĐỢI**

Sau khi push thành công:
- ✅ Code đã được upload lên GitHub
- ✅ Render tự động detect thay đổi
- ✅ Render bắt đầu redeploy
- ✅ Website sẽ hoạt động với các sửa đổi mới
- ✅ Không còn lỗi 500 Internal Server Error

---

## 📞 **HỖ TRỢ**

Nếu gặp vấn đề:
1. Chạy script tự động: `.\setup_git_and_push.ps1`
2. Kiểm tra logs trong Render dashboard
3. Đảm bảo tất cả file đã được commit
4. Kiểm tra URL repository chính xác

**Chúc bạn thành công! 🎉**
