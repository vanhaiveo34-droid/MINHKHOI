#!/usr/bin/env python3
"""
Script khởi tạo dữ liệu cho production
Chạy script này sau khi deploy để tạo dữ liệu mẫu
"""

from app_sqlite import app, db, User, Ticket
from datetime import datetime, timedelta
import random
import os

def init_production_data():
    with app.app_context():
        # Tạo database tables
        db.create_all()
        
        # Kiểm tra xem đã có dữ liệu chưa
        if User.query.first():
            print("✅ Đã có dữ liệu trong database. Bỏ qua việc tạo dữ liệu mẫu.")
            return
        
        print("🔄 Đang tạo dữ liệu mẫu cho production...")
        
        # Tạo users mẫu
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@company.com',
                'password': 'admin123',
                'role': 'quan_tri_vien'
            },
            {
                'username': 'manager',
                'email': 'manager@company.com',
                'password': 'manager123',
                'role': 'quan_ly'
            },
            {
                'username': 'sales1',
                'email': 'sales1@company.com',
                'password': 'sales123',
                'role': 'kinh_doanh'
            },
            {
                'username': 'sales2',
                'email': 'sales2@company.com',
                'password': 'sales123',
                'role': 'kinh_doanh'
            },
            {
                'username': 'tech1',
                'email': 'tech1@company.com',
                'password': 'tech123',
                'role': 'ky_thuat_vien'
            },
            {
                'username': 'tech2',
                'email': 'tech2@company.com',
                'password': 'tech123',
                'role': 'ky_thuat_vien'
            },
            {
                'username': 'tech3',
                'email': 'tech3@company.com',
                'password': 'tech123',
                'role': 'ky_thuat_vien'
            }
        ]
        
        users = {}
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            users[user_data['username']] = user
        
        db.session.commit()
        print(f"✅ Đã tạo {len(users_data)} tài khoản mẫu")
        
        # Tạo tickets mẫu
        customers = [
            {
                'name': 'Công ty ABC',
                'address': '123 Đường Nguyễn Huệ, Quận 1, TP.HCM',
                'phone': '0901 234 567'
            },
            {
                'name': 'Công ty XYZ',
                'address': '456 Đường Lê Lợi, Quận 3, TP.HCM',
                'phone': '0902 345 678'
            },
            {
                'name': 'Công ty DEF',
                'address': '789 Đường Trần Hưng Đạo, Quận 5, TP.HCM',
                'phone': '0903 456 789'
            },
            {
                'name': 'Công ty GHI',
                'address': '321 Đường Võ Văn Tần, Quận 3, TP.HCM',
                'phone': '0904 567 890'
            },
            {
                'name': 'Công ty JKL',
                'address': '654 Đường Hai Bà Trưng, Quận 1, TP.HCM',
                'phone': '0905 678 901'
            }
        ]
        
        descriptions = [
            'Sửa chữa máy tính không khởi động được',
            'Cài đặt phần mềm mới cho hệ thống',
            'Bảo trì máy chủ định kỳ',
            'Khắc phục lỗi mạng không kết nối internet',
            'Thay thế ổ cứng bị hỏng',
            'Cài đặt camera giám sát',
            'Sửa chữa máy in không in được',
            'Cấu hình router wifi mới',
            'Khắc phục lỗi phần mềm kế toán',
            'Bảo trì hệ thống điều hòa'
        ]
        
        priorities = ['thap', 'trung_binh', 'cao', 'khan_cap']
        statuses = ['cho_xu_ly', 'da_phan_cong', 'dang_xu_ly', 'hoan_thanh']
        
        tickets = []
        for i in range(15):
            # Tạo số phiếu
            date_str = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d')
            ticket_number = f"TK{date_str}{random.randint(1000, 9999)}"
            
            # Chọn ngẫu nhiên thông tin
            customer = random.choice(customers)
            description = random.choice(descriptions)
            priority = random.choice(priorities)
            status = random.choice(statuses)
            created_by = random.choice([users['sales1'], users['sales2']])
            
            # Tạo thời gian
            created_at = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            
            ticket = Ticket(
                ticket_number=ticket_number,
                customer_name=customer['name'],
                customer_address=customer['address'],
                customer_phone=customer['phone'],
                description=description,
                priority=priority,
                status=status,
                created_by=created_by.id,
                created_at=created_at
            )
            
            # Nếu phiếu đã được gán hoặc đang xử lý
            if status in ['da_phan_cong', 'dang_xu_ly', 'hoan_thanh']:
                technician = random.choice([users['tech1'], users['tech2'], users['tech3']])
                ticket.assigned_to = technician.id
                ticket.assigned_by = users['manager'].id
                ticket.assigned_at = created_at + timedelta(hours=random.randint(1, 24))
                
                if status == 'hoan_thanh':
                    ticket.completed_at = ticket.assigned_at + timedelta(hours=random.randint(1, 8))
                    ticket.completion_notes = f"Đã hoàn thành công việc. Khách hàng hài lòng với dịch vụ."
                elif status == 'dang_xu_ly':
                    ticket.completion_notes = f"Đang thực hiện công việc. Dự kiến hoàn thành trong 2-3 giờ."
            
            tickets.append(ticket)
            db.session.add(ticket)
        
        db.session.commit()
        print(f"✅ Đã tạo {len(tickets)} phiếu mẫu")
        
        print("\n🎉 KHỞI TẠO DỮ LIỆU THÀNH CÔNG!")
        print("=" * 50)
        print("🔐 THÔNG TIN ĐĂNG NHẬP:")
        print("👑 Quản trị viên: admin / admin123")
        print("👨‍💼 Quản lý: manager / manager123")
        print("💼 Kinh doanh: sales1 / sales123")
        print("🔧 Kỹ thuật viên: tech1 / tech123")
        print("\n🌐 Truy cập website để bắt đầu sử dụng!")

if __name__ == '__main__':
    init_production_data()
