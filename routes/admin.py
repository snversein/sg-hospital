from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USERNAME = 'user'
ADMIN_PASSWORD = 'admin123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('')
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    return render_template('admin_login.html')

@admin_bp.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session['admin_user'] = username
        return redirect(url_for('admin.dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('admin.login'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    from models import db, Appointment, ContactMessage
    
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    contact_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(10).all()
    
    stats = {
        'total_appointments': Appointment.query.count(),
        'pending': Appointment.query.filter_by(status='pending').count(),
        'confirmed': Appointment.query.filter_by(status='confirmed').count(),
        'completed': Appointment.query.filter_by(status='completed').count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count()
    }
    
    return render_template('admin_dashboard.html', 
                         appointments=appointments,
                         messages=contact_messages,
                         stats=stats,
                         active_page='dashboard')

@admin_bp.route('/appointments')
@login_required
def appointments():
    from models import Appointment
    all_appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin_appointments.html', appointments=all_appointments, active_page='appointments')

@admin_bp.route('/messages')
@login_required
def messages():
    from models import ContactMessage
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_messages.html', messages=all_messages, active_page='messages')

@admin_bp.route('/patients')
@login_required
def patients():
    from models import Appointment
    # Get unique patients based on phone number
    all_apts = Appointment.query.order_by(Appointment.created_at.desc()).all()
    seen_phones = set()
    unique_patients = []
    for apt in all_apts:
        if apt.phone not in seen_phones:
            unique_patients.append(apt)
            seen_phones.add(apt.phone)
    
    return render_template('admin_patients.html', patients=unique_patients, active_page='patients')
