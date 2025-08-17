from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server')
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
    role = db.Column(db.String(20), nullable=False, default='technician')  # admin, sales, technician, manager
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
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='pending')  # pending, assigned, in_progress, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    completion_notes = db.Column(db.Text, nullable=True)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    technician = db.relationship('User', foreign_keys=[assigned_to])
    assigner = db.relationship('User', foreign_keys=[assigned_by])

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
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'technician')
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại!', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
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
    if current_user.role == 'admin':
        tickets = Ticket.query.all()
    elif current_user.role == 'manager':
        tickets = Ticket.query.filter(Ticket.status.in_(['pending', 'assigned'])).all()
    elif current_user.role == 'sales':
        tickets = Ticket.query.filter_by(created_by=current_user.id).all()
    else:  # technician
        tickets = Ticket.query.filter_by(assigned_to=current_user.id).all()
    
    return render_template('dashboard.html', tickets=tickets)

@app.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if current_user.role not in ['sales', 'admin']:
        flash('Bạn không có quyền tạo phiếu!', 'error')
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
        
        flash('Tạo phiếu thành công!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('new_ticket.html')

@app.route('/tickets/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign_ticket(ticket_id):
    if current_user.role not in ['manager', 'admin']:
        flash('Bạn không có quyền điều phiếu!', 'error')
        return redirect(url_for('dashboard'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    technician_id = request.form.get('technician_id')
    
    if technician_id:
        technician = User.query.filter_by(id=technician_id, role='technician').first()
        if technician:
            ticket.assigned_to = technician.id
            ticket.assigned_by = current_user.id
            ticket.assigned_at = datetime.utcnow()
            ticket.status = 'assigned'
            db.session.commit()
            flash('Điều phiếu thành công!', 'success')
        else:
            flash('Không tìm thấy kỹ thuật viên!', 'error')
    else:
        flash('Vui lòng chọn kỹ thuật viên!', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/tickets/<int:ticket_id>/update_status', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.role == 'technician' and ticket.assigned_to != current_user.id:
        flash('Bạn không có quyền cập nhật phiếu này!', 'error')
        return redirect(url_for('dashboard'))
    
    status = request.form.get('status')
    completion_notes = request.form.get('completion_notes', '')
    
    ticket.status = status
    if status == 'completed':
        ticket.completed_at = datetime.utcnow()
        ticket.completion_notes = completion_notes
    elif status == 'in_progress':
        ticket.completion_notes = completion_notes
    
    db.session.commit()
    flash('Cập nhật trạng thái thành công!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/technicians')
@login_required
def get_technicians():
    if current_user.role not in ['manager', 'admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    technicians = User.query.filter_by(role='technician').all()
    return jsonify([{'id': t.id, 'username': t.username} for t in technicians])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
