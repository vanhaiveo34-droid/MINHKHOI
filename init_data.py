#!/usr/bin/env python3
"""
Script khởi tạo dữ liệu mẫu cho hệ thống quản lý phiếu kỹ thuật
"""

try:
    from app import app, db, User, Ticket
except ImportError:
    from app_sqlite import app, db, User, Ticket
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Tạo database tables
        db.create_all()
        
            # Kiểm tra xem đã có dữ liệu chưa
    # if User.query.first():
    #     print("Đã có dữ liệu trong database. Bỏ qua việc tạo dữ liệu mẫu.")
    #     return
        
        print("Đang tạo dữ liệu mẫu...")
        
        # Tạo users mẫu
        users_data = [
            {
                'username': 'quan_tri_vien',
                'email': 'quan_tri_vien@company.com',
                'password': 'quan_tri_vien123',
                'role': 'quan_tri_vien'
            },
            {
                'username': 'quan_ly1',
                'email': 'quan_ly1@company.com',
                'password': 'quan_ly123',
                'role': 'quan_ly'
            },
            {
                'username': 'kinh_doanh1',
                'email': 'kinh_doanh1@company.com',
                'password': 'kinh_doanh123',
                'role': 'kinh_doanh'
            },
            {
                'username': 'kinh_doanh2',
                'email': 'kinh_doanh2@company.com',
                'password': 'kinh_doanh123',
                'role': 'kinh_doanh'
            },
            {
                'username': 'ky_thuat1',
                'email': 'ky_thuat1@company.com',
                'password': 'ky_thuat123',
                'role': 'ky_thuat_vien'
            },
            {
                'username': 'ky_thuat2',
                'email': 'ky_thuat2@company.com',
                'password': 'ky_thuat123',
                'role': 'ky_thuat_vien'
            },
            {
                'username': 'ky_thuat3',
                'email': 'ky_thuat3@company.com',
                'password': 'ky_thuat123',
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
        print(f"Đã tạo {len(users_data)} tài khoản mẫu")
        
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
        for i in range(20):
            # Tạo số phiếu
            date_str = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d')
            ticket_number = f"TK{date_str}{random.randint(1000, 9999)}"
            
            # Chọn ngẫu nhiên thông tin
            customer = random.choice(customers)
            description = random.choice(descriptions)
            priority = random.choice(priorities)
            status = random.choice(statuses)
            created_by = random.choice([users['kinh_doanh1'], users['kinh_doanh2']])
            
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
                technician = random.choice([users['ky_thuat1'], users['ky_thuat2'], users['ky_thuat3']])
                ticket.assigned_to = technician.id
                ticket.assigned_by = users['quan_ly1'].id
                ticket.assigned_at = created_at + timedelta(hours=random.randint(1, 24))
                
                if status == 'hoan_thanh':
                    ticket.completed_at = ticket.assigned_at + timedelta(hours=random.randint(1, 8))
                    ticket.completion_notes = f"Đã hoàn thành công việc. Khách hàng hài lòng với dịch vụ."
                elif status == 'dang_xu_ly':
                    ticket.completion_notes = f"Đang thực hiện công việc. Dự kiến hoàn thành trong 2-3 giờ."
            
            tickets.append(ticket)
            db.session.add(ticket)
        
        db.session.commit()
        print(f"Đã tạo {len(tickets)} phiếu mẫu")
        
        print("\n=== THÔNG TIN ĐĂNG NHẬP MẪU ===")
        print("Quản trị viên: quan_tri_vien / quan_tri_vien123")
        print("Quản lý: quan_ly1 / quan_ly123")
        print("Kinh doanh: kinh_doanh1 / kinh_doanh123")
        print("Kỹ thuật viên: ky_thuat1 / ky_thuat123")
        print("\nTruy cập http://localhost:5000 để bắt đầu sử dụng!")

if __name__ == '__main__':
    create_sample_data()
