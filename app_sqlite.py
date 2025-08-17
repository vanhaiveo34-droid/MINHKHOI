from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

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
    role = db.Column(db.String(20), nullable=False, default='ky_thuat_vien')  # quan_tri_vien, kinh_doanh, ky_thuat_vien, quan_ly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='trung_binh')  # thap, trung_binh, cao, khan_cap
    status = db.Column(db.String(20), default='cho_xu_ly')  # cho_xu_ly, da_phan_cong, dang_xu_ly, hoan_thanh, da_huy
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
        role = request.form.get('role', 'technician')
        
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
        import random
        ticket_number = f"TK{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        ticket = Ticket(
            ticket_number=ticket_number,
            customer_name=request.form.get('customer_name'),
            customer_address=request.form.get('customer_address'),
            customer_phone=request.form.get('customer_phone'),
            description=request.form.get('description'),
            priority=request.form.get('priority'),
            created_by=current_user.id
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        flash('Tạo phiếu thành công!', 'thanh_cong')
        return redirect(url_for('dashboard'))
    
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
    
    # Chỉ cho phép người tạo phiếu hoặc quản trị viên xóa
    if current_user.role not in ['quan_tri_vien'] and ticket.created_by != current_user.id:
        flash('Bạn không có quyền xóa phiếu này!', 'loi')
        return redirect(url_for('dashboard'))
    
    # Thêm thông tin xóa
    ticket.deleted_at = datetime.utcnow()
    ticket.deleted_by = current_user.id
    ticket.status = 'da_huy'
    db.session.commit()
    
    flash('Đã xóa phiếu thành công!', 'thanh_cong')
    return redirect(url_for('dashboard'))

@app.route('/tickets/search')
@login_required
def search_tickets():
    search_term = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    # Base query theo role
    if current_user.role == 'quan_tri_vien':
        query = Ticket.query
    elif current_user.role == 'quan_ly':
        query = Ticket.query.filter(Ticket.status.in_(['cho_xu_ly', 'da_phan_cong']))
    elif current_user.role == 'kinh_doanh':
        query = Ticket.query.filter_by(created_by=current_user.id)
    else:  # ky_thuat_vien
        query = Ticket.query.filter_by(assigned_to=current_user.id)
    
    # Áp dụng bộ lọc
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

@app.route('/tickets/<int:ticket_id>/update_status', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.role == 'ky_thuat_vien' and ticket.assigned_to != current_user.id:
        flash('Bạn không có quyền cập nhật phiếu này!', 'loi')
        return redirect(url_for('dashboard'))
    
    status = request.form.get('status')
    completion_notes = request.form.get('completion_notes', '')
    
    ticket.status = status
    if status == 'hoan_thanh':
        ticket.completed_at = datetime.utcnow()
        ticket.completion_notes = completion_notes
    elif status == 'dang_xu_ly':
        ticket.completion_notes = completion_notes
    
    db.session.commit()
    flash('Cập nhật trạng thái thành công!', 'thanh_cong')
    return redirect(url_for('dashboard'))

@app.route('/api/technicians')
@login_required
def get_technicians():
    if current_user.role not in ['quan_ly', 'quan_tri_vien']:
        return jsonify({'loi': 'Không có quyền truy cập'}), 403
    
    technicians = User.query.filter_by(role='ky_thuat_vien').all()
    return jsonify([{'id': t.id, 'username': t.username} for t in technicians])

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền truy cập trang này!', 'loi')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.role, User.username).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'quan_tri_vien':
        flash('Bạn không có quyền thực hiện hành động này!', 'loi')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Không cho phép xóa chính mình
    if user.id == current_user.id:
        flash('Không thể xóa tài khoản của chính mình!', 'loi')
        return redirect(url_for('admin_users'))
    
    # Kiểm tra xem user có phiếu nào không
    tickets_created = Ticket.query.filter_by(created_by=user.id).count()
    tickets_assigned = Ticket.query.filter_by(assigned_to=user.id).count()
    
    if tickets_created > 0 or tickets_assigned > 0:
        flash(f'Không thể xóa người dùng này vì họ có {tickets_created + tickets_assigned} phiếu liên quan!', 'loi')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Đã xóa người dùng thành công!', 'thanh_cong')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Sử dụng port từ environment variable hoặc mặc định 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
