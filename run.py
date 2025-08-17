#!/usr/bin/env python3
"""
File khởi động server duy nhất cho hệ thống quản lý phiếu kỹ thuật
Chạy: py run.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mat-khau-bi-mat-thay-doi-trong-moi-truong-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='ky_thuat_vien')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_location = db.Column(db.Text, nullable=True)  # Định vị công ty khách
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='trung_binh')
    status = db.Column(db.String(20), default='cho_xu_ly')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_at = db.Column(db.DateTime, nullable=True)
    accepted_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    completion_notes = db.Column(db.Text, nullable=True)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    technician = db.relationship('User', foreign_keys=[assigned_to])
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    deleter = db.relationship('User', foreign_keys=[deleted_by])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'loi')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'ky_thuat_vien')
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'loi')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại!', 'loi')
            return render_template('register.html')
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'thanh_cong')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'quan_tri_vien':
        tickets = Ticket.query.all()
    elif current_user.role == 'quan_ly':
        tickets = Ticket.query.filter(Ticket.status.in_(['cho_xu_ly', 'da_phan_cong'])).all()
    elif current_user.role == 'kinh_doanh':
        tickets = Ticket.query.filter_by(created_by=current_user.id).all()
    else:  # ky_thuat_vien
        tickets = Ticket.query.filter_by(assigned_to=current_user.id).all()
    
    return render_template('dashboard.html', tickets=tickets)

@app.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if current_user.role not in ['kinh_doanh', 'quan_tri_vien']:
        flash('Bạn không có quyền tạo phiếu!', 'loi')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_address = request.form.get('customer_address')
        customer_phone = request.form.get('customer_phone')
        customer_location = request.form.get('customer_location')
        description = request.form.get('description')
        priority = request.form.get('priority')
        
        # Kiểm tra dữ liệu đầu vào
        if not customer_name or not customer_address or not customer_phone or not description:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc!', 'loi')
            return render_template('new_ticket.html')
        
        try:
            # Tạo số phiếu duy nhất
            ticket_number = f"TK{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
            
            # Kiểm tra số phiếu đã tồn tại (rất hiếm khi xảy ra)
            while Ticket.query.filter_by(ticket_number=ticket_number).first():
                ticket_number = f"TK{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
            
            # Tạo phiếu mới
            ticket = Ticket(
                ticket_number=ticket_number,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_phone=customer_phone,
                customer_location=customer_location,
                description=description,
                priority=priority or 'trung_binh',
                created_by=current_user.id
            )
            
            # Lưu vào database
            db.session.add(ticket)
            db.session.commit()
            
            flash(f'Tạo phiếu {ticket_number} thành công!', 'thanh_cong')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra khi tạo phiếu: {str(e)}', 'loi')
            return render_template('new_ticket.html')
    
    return render_template('new_ticket.html')

@app.route('/tickets/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign_ticket(ticket_id):
    if current_user.role not in ['quan_ly', 'quan_tri_vien']:
        flash('Bạn không có quyền điều phiếu!', 'loi')
        return redirect(url_for('dashboard'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    technician_id = request.form.get('technician_id')
    
    if technician_id:
        technician = User.query.filter_by(id=technician_id, role='ky_thuat_vien').first()
        if technician:
            ticket.assigned_to = technician.id
            ticket.assigned_by = current_user.id
            ticket.assigned_at = datetime.utcnow()
            ticket.status = 'da_phan_cong'
            db.session.commit()
            flash('Điều phiếu thành công!', 'thanh_cong')
        else:
            flash('Không tìm thấy kỹ thuật viên!', 'loi')
    else:
        flash('Vui lòng chọn kỹ thuật viên!', 'loi')
    
    return redirect(url_for('dashboard'))

@app.route('/tickets/<int:ticket_id>/accept', methods=['POST'])
@login_required
def accept_ticket(ticket_id):
    if current_user.role != 'ky_thuat_vien':
        flash('Bạn không có quyền nhận phiếu!', 'loi')
        return redirect(url_for('dashboard'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.assigned_to != current_user.id:
        flash('Phiếu này không được gán cho bạn!', 'loi')
        return redirect(url_for('dashboard'))
    
    ticket.status = 'dang_xu_ly'
    ticket.accepted_at = datetime.utcnow()
    db.session.commit()
    flash('Đã nhận phiếu thành công!', 'thanh_cong')
    return redirect(url_for('dashboard'))

@app.route('/tickets/<int:ticket_id>/complete', methods=['POST'])
@login_required
def complete_ticket(ticket_id):
    if current_user.role != 'ky_thuat_vien':
        flash('Bạn không có quyền hoàn thành phiếu!', 'loi')
        return redirect(url_for('dashboard'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.assigned_to != current_user.id:
        flash('Phiếu này không được gán cho bạn!', 'loi')
        return redirect(url_for('dashboard'))
    
    completion_notes = request.form.get('completion_notes', '')
    ticket.status = 'hoan_thanh'
    ticket.completed_at = datetime.utcnow()
    ticket.completion_notes = completion_notes
    db.session.commit()
    flash('Hoàn thành phiếu thành công!', 'thanh_cong')
    return redirect(url_for('dashboard'))

@app.route('/tickets/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.role not in ['quan_tri_vien'] and ticket.created_by != current_user.id:
        flash('Bạn không có quyền xóa phiếu này!', 'loi')
        return redirect(url_for('dashboard'))
    
    # Xóa thực sự phiếu khỏi database
    db.session.delete(ticket)
    db.session.commit()
    
    flash('Đã xóa phiếu thành công!', 'thanh_cong')
    return redirect(url_for('dashboard'))

@app.route('/tickets/search')
@login_required
def search_tickets():
    search_term = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    if current_user.role == 'quan_tri_vien':
        query = Ticket.query
    elif current_user.role == 'quan_ly':
        query = Ticket.query.filter(Ticket.status.in_(['cho_xu_ly', 'da_phan_cong']))
    elif current_user.role == 'kinh_doanh':
        query = Ticket.query.filter_by(created_by=current_user.id)
    else:  # ky_thuat_vien
        query = Ticket.query.filter_by(assigned_to=current_user.id)
    
    if search_term:
        query = query.filter(
            db.or_(
                Ticket.ticket_number.contains(search_term),
                Ticket.customer_name.contains(search_term),
                Ticket.description.contains(search_term)
            )
        )
    
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    
    if priority_filter:
        query = query.filter(Ticket.priority == priority_filter)
    
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return render_template('dashboard.html', tickets=tickets)

@app.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    """Chỉnh sửa thông tin phiếu"""
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Chỉ cho phép người tạo phiếu, quản lý và quản trị viên chỉnh sửa
    if current_user.role not in ['quan_tri_vien', 'quan_ly'] and ticket.created_by != current_user.id:
        flash('Bạn không có quyền chỉnh sửa phiếu này!', 'loi')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_address = request.form.get('customer_address')
        customer_phone = request.form.get('customer_phone')
        customer_location = request.form.get('customer_location')
        description = request.form.get('description')
        priority = request.form.get('priority')
        
        # Kiểm tra dữ liệu đầu vào
        if not customer_name or not customer_address or not customer_phone or not description:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc!', 'loi')
            return render_template('edit_ticket.html', ticket=ticket)
        
        try:
            # Cập nhật thông tin phiếu
            ticket.customer_name = customer_name
            ticket.customer_address = customer_address
            ticket.customer_phone = customer_phone
            ticket.customer_location = customer_location
            ticket.description = description
            ticket.priority = priority or 'trung_binh'
            ticket.status = 'cho_xu_ly'  # Đưa về trạng thái chờ xử lý
            
            # Lưu vào database
            db.session.commit()
            
            flash(f'Chỉnh sửa phiếu {ticket.ticket_number} thành công!', 'thanh_cong')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra khi chỉnh sửa phiếu: {str(e)}', 'loi')
            return render_template('edit_ticket.html', ticket=ticket)
    
    return render_template('edit_ticket.html', ticket=ticket)

@app.route('/tickets/<int:ticket_id>/update_status', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.role == 'ky_thuat_vien' and ticket.assigned_to != current_user.id:
        flash('Bạn không có quyền cập nhật phiếu này!', 'loi')
        return redirect(url_for('dashboard'))
    
    status = request.form.get('status')
    completion_notes = request.form.get('completion_notes', '')
    
    # Kiểm tra trạng thái hợp lệ
    valid_statuses = ['cho_xu_ly', 'da_phan_cong', 'dang_xu_ly', 'hoan_thanh', 'da_huy']
    if status not in valid_statuses:
        flash('Trạng thái không hợp lệ!', 'loi')
        return redirect(url_for('dashboard'))
    
    try:
        # Cập nhật trạng thái
        ticket.status = status
        
        # Cập nhật thời gian và ghi chú theo trạng thái
        if status == 'hoan_thanh':
            ticket.completed_at = datetime.utcnow()
            ticket.completion_notes = completion_notes
        elif status == 'dang_xu_ly':
            ticket.completion_notes = completion_notes
        elif status == 'da_huy':
            ticket.completion_notes = completion_notes
        
        # Lưu vào database
        db.session.commit()
        
        flash(f'Cập nhật trạng thái phiếu {ticket.ticket_number} thành công!', 'thanh_cong')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra khi cập nhật trạng thái: {str(e)}', 'loi')
        return redirect(url_for('dashboard'))

@app.route('/api/technicians')
@login_required
def get_technicians():
    if current_user.role not in ['quan_ly', 'quan_tri_vien']:
        return jsonify({'loi': 'Không có quyền truy cập'}), 403
    
    # Chỉ lấy kỹ thuật viên đang online
    technicians = User.query.filter_by(role='ky_thuat_vien', is_online=True).all()
    return jsonify([{'id': t.id, 'username': t.username} for t in technicians])

@app.route('/api/update_status', methods=['POST'])
@login_required
def update_user_status():
    """Cập nhật trạng thái online/offline của user"""
    is_online = request.json.get('is_online', False)
    current_user.is_online = is_online
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/online_users')
@login_required
def get_online_users():
    """Lấy danh sách user đang online"""
    if current_user.role != 'quan_tri_vien':
        return jsonify({'loi': 'Không có quyền truy cập'}), 403
    
    online_users = User.query.filter_by(is_online=True).all()
    return jsonify([{
        'id': u.id, 
        'username': u.username, 
        'role': u.role, 
        'last_seen': u.last_seen.strftime('%d/%m/%Y %H:%M') if u.last_seen else None
    } for u in online_users])

@app.route('/admin/users')
@login_required
def admin_users():
    """Trang quản lý nhân viên (chỉ quản trị viên)"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền truy cập trang này!', 'loi')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """Thêm nhân viên mới"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền thêm nhân viên!', 'loi')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Kiểm tra dữ liệu đầu vào
        if not username or not email or not password or not role:
            flash('Vui lòng điền đầy đủ thông tin!', 'loi')
            return render_template('add_user.html')
        
        # Kiểm tra username đã tồn tại
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'loi')
            return render_template('add_user.html')
        
        # Kiểm tra email đã tồn tại
        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại!', 'loi')
            return render_template('add_user.html')
        
        try:
            # Tạo user mới
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            
            # Thêm vào database
            db.session.add(user)
            db.session.commit()
            
            flash(f'Thêm nhân viên "{username}" thành công!', 'thanh_cong')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra khi thêm nhân viên: {str(e)}', 'loi')
            return render_template('add_user.html')
    
    return render_template('add_user.html')

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Chỉnh sửa thông tin nhân viên"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền chỉnh sửa nhân viên!', 'loi')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        
        # Kiểm tra dữ liệu đầu vào
        if not username or not email or not role:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc!', 'loi')
            return render_template('edit_user.html', user=user)
        
        # Kiểm tra username đã tồn tại (trừ user hiện tại)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            flash('Tên đăng nhập đã tồn tại!', 'loi')
            return render_template('edit_user.html', user=user)
        
        # Kiểm tra email đã tồn tại (trừ user hiện tại)
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != user.id:
            flash('Email đã tồn tại!', 'loi')
            return render_template('edit_user.html', user=user)
        
        try:
            # Cập nhật thông tin
            user.username = username
            user.email = email
            user.role = role
            
            # Cập nhật mật khẩu nếu có
            if password:
                user.set_password(password)
            
            # Lưu vào database
            db.session.commit()
            
            flash(f'Cập nhật nhân viên "{username}" thành công!', 'thanh_cong')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra khi cập nhật nhân viên: {str(e)}', 'loi')
            return render_template('edit_user.html', user=user)
    
    return render_template('edit_user.html', user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Xóa nhân viên"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền xóa nhân viên!', 'loi')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Không thể xóa chính mình!', 'loi')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Xóa nhân viên thành công!', 'thanh_cong')
    return redirect(url_for('admin_users'))

@app.route('/admin/password-management')
@login_required
def password_management():
    """Trang quản lý mật khẩu"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền truy cập trang này!', 'loi')
        return redirect(url_for('dashboard'))
    
    search_term = request.args.get('search', '')
    
    if search_term:
        users = User.query.filter(
            db.or_(
                User.username.contains(search_term),
                User.email.contains(search_term)
            )
        ).all()
    else:
        users = User.query.all()
    
    return render_template('password_management.html', users=users)

@app.route('/admin/reset-password', methods=['POST'])
@login_required
def reset_user_password():
    """Đặt lại mật khẩu cho user"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền thực hiện thao tác này!', 'loi')
        return redirect(url_for('dashboard'))
    
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    
    if not user_id or not new_password:
        flash('Thiếu thông tin cần thiết!', 'loi')
        return redirect(url_for('password_management'))
    
    try:
        user = User.query.get_or_404(user_id)
        user.set_password(new_password)
        db.session.commit()
        
        flash(f'Đã đặt lại mật khẩu cho "{user.username}" thành công! Mật khẩu mới: {new_password}', 'thanh_cong')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra khi đặt lại mật khẩu: {str(e)}', 'loi')
    
    return redirect(url_for('password_management'))

@app.route('/admin/change-password', methods=['POST'])
@login_required
def change_user_password():
    """Thay đổi mật khẩu cho user (cần mật khẩu hiện tại)"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền thực hiện thao tác này!', 'loi')
        return redirect(url_for('dashboard'))
    
    user_id = request.form.get('user_id')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([user_id, current_password, new_password, confirm_password]):
        flash('Vui lòng điền đầy đủ thông tin!', 'loi')
        return redirect(url_for('password_management'))
    
    if new_password != confirm_password:
        flash('Mật khẩu mới và xác nhận mật khẩu không khớp!', 'loi')
        return redirect(url_for('password_management'))
    
    try:
        user = User.query.get_or_404(user_id)
        
        # Kiểm tra mật khẩu hiện tại
        if not user.check_password(current_password):
            flash('Mật khẩu hiện tại không đúng!', 'loi')
            return redirect(url_for('password_management'))
        
        # Kiểm tra độ mạnh mật khẩu
        if len(new_password) < 6:
            flash('Mật khẩu mới phải có ít nhất 6 ký tự!', 'loi')
            return redirect(url_for('password_management'))
        
        user.set_password(new_password)
        db.session.commit()
        
        flash(f'Đã thay đổi mật khẩu cho "{user.username}" thành công!', 'thanh_cong')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra khi thay đổi mật khẩu: {str(e)}', 'loi')
    
    return redirect(url_for('password_management'))

@app.route('/admin/force-logout', methods=['POST'])
@login_required
def force_logout_user():
    """Đăng xuất cưỡng bức user"""
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền thực hiện thao tác này!', 'loi')
        return redirect(url_for('dashboard'))
    
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('Thiếu thông tin user!', 'loi')
        return redirect(url_for('password_management'))
    
    try:
        user = User.query.get_or_404(user_id)
        
        # Đặt trạng thái offline
        user.is_online = False
        user.last_seen = datetime.utcnow()
        db.session.commit()
        
        flash(f'Đã đăng xuất cưỡng bức tài khoản "{user.username}"!', 'thanh_cong')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra khi đăng xuất: {str(e)}', 'loi')
    
    return redirect(url_for('password_management'))

def create_sample_data():
    """Tạo dữ liệu mẫu nếu chưa có"""
    if User.query.first():
        return  # Đã có dữ liệu
    
    print("Đang tạo dữ liệu mẫu...")
    
    # Tạo users mẫu
    users_data = [
        {'username': 'quan_tri_vien', 'email': 'quan_tri_vien@company.com', 'password': 'quan_tri_vien123', 'role': 'quan_tri_vien'},
        {'username': 'quan_ly1', 'email': 'quan_ly1@company.com', 'password': 'quan_ly123', 'role': 'quan_ly'},
        {'username': 'kinh_doanh1', 'email': 'kinh_doanh1@company.com', 'password': 'kinh_doanh123', 'role': 'kinh_doanh'},
        {'username': 'kinh_doanh2', 'email': 'kinh_doanh2@company.com', 'password': 'kinh_doanh123', 'role': 'kinh_doanh'},
        {'username': 'ky_thuat1', 'email': 'ky_thuat1@company.com', 'password': 'ky_thuat123', 'role': 'ky_thuat_vien'},
        {'username': 'ky_thuat2', 'email': 'ky_thuat2@company.com', 'password': 'ky_thuat123', 'role': 'ky_thuat_vien'},
        {'username': 'ky_thuat3', 'email': 'ky_thuat3@company.com', 'password': 'ky_thuat123', 'role': 'ky_thuat_vien'}
    ]
    
    users = {}
    for user_data in users_data:
        user = User(username=user_data['username'], email=user_data['email'], role=user_data['role'])
        user.set_password(user_data['password'])
        
        # Set kỹ thuật viên mặc định là online
        if user_data['role'] == 'ky_thuat_vien':
            user.is_online = True
        
        db.session.add(user)
        users[user_data['username']] = user
    
    db.session.commit()
    print(f"Đã tạo {len(users_data)} tài khoản mẫu")
    
    # Tạo tickets mẫu
    customers = [
        {'name': 'Công ty ABC', 'address': '123 Đường Nguyễn Huệ, Quận 1, TP.HCM', 'phone': '0901 234 567', 'location': '10.7769, 106.7009'},
        {'name': 'Công ty XYZ', 'address': '456 Đường Lê Lợi, Quận 3, TP.HCM', 'phone': '0902 345 678', 'location': '10.7827, 106.6891'},
        {'name': 'Công ty DEF', 'address': '789 Đường Trần Hưng Đạo, Quận 5, TP.HCM', 'phone': '0903 456 789', 'location': '10.7544, 106.6624'}
    ]
    
    descriptions = [
        'Sửa chữa máy tính không khởi động được',
        'Cài đặt phần mềm mới cho hệ thống',
        'Bảo trì máy chủ định kỳ',
        'Khắc phục lỗi mạng không kết nối internet'
    ]
    
    priorities = ['thap', 'trung_binh', 'cao', 'khan_cap']
    statuses = ['cho_xu_ly', 'da_phan_cong', 'dang_xu_ly', 'hoan_thanh']
    
    for i in range(10):
        date_str = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d')
        ticket_number = f"TK{date_str}{random.randint(1000, 9999)}"
        
        customer = random.choice(customers)
        description = random.choice(descriptions)
        priority = random.choice(priorities)
        status = random.choice(statuses)
        created_by = random.choice([users['kinh_doanh1'], users['kinh_doanh2']])
        
        created_at = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        ticket = Ticket(
            ticket_number=ticket_number,
            customer_name=customer['name'],
            customer_address=customer['address'],
            customer_phone=customer['phone'],
            customer_location=customer['location'],
            description=description,
            priority=priority,
            status=status,
            created_by=created_by.id,
            created_at=created_at
        )
        
        if status in ['da_phan_cong', 'dang_xu_ly', 'hoan_thanh']:
            technician = random.choice([users['ky_thuat1'], users['ky_thuat2'], users['ky_thuat3']])
            ticket.assigned_to = technician.id
            ticket.assigned_by = users['quan_ly1'].id
            ticket.assigned_at = created_at + timedelta(hours=random.randint(1, 24))
            
            if status == 'hoan_thanh':
                ticket.completed_at = ticket.assigned_at + timedelta(hours=random.randint(1, 8))
                ticket.completion_notes = "Đã hoàn thành công việc. Khách hàng hài lòng với dịch vụ."
            elif status == 'dang_xu_ly':
                ticket.completion_notes = "Đang thực hiện công việc. Dự kiến hoàn thành trong 2-3 giờ."
        
        db.session.add(ticket)
    
    db.session.commit()
    print(f"Đã tạo 10 phiếu mẫu")
    
    print("\n=== THÔNG TIN ĐĂNG NHẬP MẪU ===")
    print("Quản trị viên: quan_tri_vien / quan_tri_vien123")
    print("Quản lý: quan_ly1 / quan_ly123")
    print("Kinh doanh: kinh_doanh1 / kinh_doanh123")
    print("Kỹ thuật viên: ky_thuat1 / ky_thuat123")
    print("\nTruy cập http://localhost:5000 để bắt đầu sử dụng!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    print("🚀 Khởi động server thành công!")
    print("🌐 Truy cập: http://localhost:5000")
    print("📱 Ứng dụng hỗ trợ cả máy tính và điện thoại")
    print("⏹️  Nhấn Ctrl+C để dừng server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
