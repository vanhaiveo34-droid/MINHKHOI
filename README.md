# HỆ THỐNG ĐIỀU PHIẾU MINH KHÔI

## 📋 Mô tả
Hệ thống điều phiếu Minh Khôi là một ứng dụng web quản lý phiếu công việc, cho phép tạo, phân công và theo dõi các phiếu dịch vụ kỹ thuật. Hệ thống được thiết kế với giao diện hiện đại, dễ sử dụng và hỗ trợ đa vai trò người dùng.

## ✨ Tính năng chính

### 🔐 Hệ thống xác thực
- **Đăng nhập/Đăng ký**: Hỗ trợ đa vai trò người dùng
- **Phân quyền**: 5 vai trò khác nhau với quyền hạn riêng biệt
- **Bảo mật**: Mã quản trị để tạo tài khoản mới

### 📊 Dashboard
- **Thống kê tổng quan**: Hiển thị số lượng phiếu theo trạng thái
- **Bộ lọc thông minh**: Tìm kiếm theo tên khách hàng, lọc theo trạng thái và độ ưu tiên
- **Xuất dữ liệu**: Tải xuống danh sách phiếu dưới dạng CSV

### 🎫 Quản lý phiếu
- **Tạo phiếu mới**: Form nhập liệu đầy đủ thông tin khách hàng
- **Điều phiếu**: Phân công phiếu cho kỹ thuật viên
- **Theo dõi trạng thái**: Cập nhật tiến độ xử lý phiếu
- **Hoàn thành phiếu**: Ghi chú và đánh dấu hoàn thành

### 👥 Quản lý nhân viên
- **Thêm nhân viên**: Tạo tài khoản mới cho nhân viên
- **Chỉnh sửa thông tin**: Cập nhật thông tin cá nhân
- **Xóa nhân viên**: Quản lý danh sách nhân viên
- **Phân vai trò**: Gán vai trò phù hợp cho từng nhân viên

## 👤 Vai trò người dùng

### 🔧 Kỹ thuật viên
- Xem phiếu được phân công
- Cập nhật trạng thái phiếu
- Hoàn thành phiếu với ghi chú
- Xem thông tin cá nhân

### 💼 Kinh doanh
- Tạo phiếu mới
- Xem tất cả phiếu
- Xóa phiếu (có quyền)
- Quản lý thông tin khách hàng

### 📊 Kế toán
- Xem thống kê phiếu
- Theo dõi tiến độ công việc
- Xuất báo cáo

### 👨‍💼 Quản lý
- Quản lý nhân viên
- Phân công công việc
- Giám sát hiệu suất

### 🔑 Quản trị viên
- **Toàn quyền hệ thống**
- Tạo/xóa/chỉnh sửa nhân viên
- Điều phiếu cho kỹ thuật viên
- Xóa phiếu
- Quản lý tất cả chức năng

## 🎨 Giao diện

### Thiết kế hiện đại
- **Gradient background**: Tạo hiệu ứng đẹp mắt
- **Glass morphism**: Hiệu ứng kính mờ cho các card
- **Responsive**: Tương thích với mọi thiết bị
- **Animation**: Hiệu ứng hover và transition mượt mà

### Màu sắc và trạng thái
- **Độ ưu tiên**: Thấp (xanh), Trung bình (vàng), Cao (đỏ), Khẩn cấp (đỏ đậm)
- **Trạng thái phiếu**: Chờ xử lý, Đã phân công, Đang xử lý, Hoàn thành, Đã hủy
- **Vai trò**: Màu sắc riêng cho từng vai trò

## 🚀 Cách sử dụng

### 1. Đăng nhập
```
Tài khoản mẫu:
- Admin: admin / admin123
- Kỹ thuật viên: technician1 / tech123
- Kinh doanh: user1 / user123
- Kế toán: accountant1 / acc123
```

### 2. Tạo phiếu mới
1. Chuyển đến tab "Tạo phiếu"
2. Điền đầy đủ thông tin khách hàng
3. Chọn độ ưu tiên
4. Nhấn "Tạo phiếu"

### 3. Điều phiếu (Admin)
1. Từ Dashboard, nhấn "Điều phiếu" trên phiếu cần phân công
2. Chọn kỹ thuật viên từ danh sách
3. Xác nhận điều phiếu

### 4. Xử lý phiếu (Kỹ thuật viên)
1. Nhận phiếu được phân công
2. Cập nhật trạng thái "Đang xử lý"
3. Hoàn thành với ghi chú

## 💾 Lưu trữ dữ liệu
- **LocalStorage**: Lưu trữ dữ liệu cục bộ trên trình duyệt
- **Tự động lưu**: Dữ liệu được lưu tự động khi có thay đổi
- **Khôi phục**: Dữ liệu được khôi phục khi tải lại trang

## 🔧 Công nghệ sử dụng
- **HTML5**: Cấu trúc trang web
- **CSS3**: Styling và animation
- **JavaScript**: Logic xử lý và tương tác
- **Font Awesome**: Icon library
- **LocalStorage API**: Lưu trữ dữ liệu

## 📱 Responsive Design
- **Desktop**: Giao diện đầy đủ với grid layout
- **Tablet**: Tối ưu cho màn hình trung bình
- **Mobile**: Layout dọc, nút to dễ nhấn

## 🔒 Bảo mật
- **Mã quản trị**: Chỉ admin mới biết mã để tạo tài khoản
- **Phân quyền**: Mỗi vai trò có quyền hạn riêng
- **Validation**: Kiểm tra dữ liệu đầu vào

## 📈 Tính năng nâng cao
- **Tìm kiếm thông minh**: Tìm theo số phiếu hoặc tên khách hàng
- **Bộ lọc đa tiêu chí**: Lọc theo trạng thái và độ ưu tiên
- **Xuất Excel**: Tải xuống báo cáo CSV
- **Thống kê real-time**: Cập nhật số liệu theo thời gian thực

## 🎯 Mục tiêu
Hệ thống được thiết kế để:
- Tối ưu hóa quy trình điều phiếu
- Tăng hiệu suất làm việc
- Theo dõi tiến độ công việc
- Quản lý nhân viên hiệu quả
- Cung cấp báo cáo chi tiết

## 📞 Hỗ trợ
Đây là phiên bản Demo của hệ thống điều phiếu Minh Khôi. Để biết thêm thông tin hoặc hỗ trợ kỹ thuật, vui lòng liên hệ đội phát triển.

---
*Phiên bản: Demo*  
*Ngôn ngữ: Tiếng Việt*  
*Cập nhật lần cuối: 2025*
*Được viết bởi: Hải Ú*
