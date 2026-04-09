from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Appointment

appointments_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

@appointments_bp.route('', methods=['GET'])
def get_appointments():
    try:
        appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        return jsonify({
            'success': True,
            'data': appointment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@appointments_bp.route('', methods=['POST'])
def create_appointment():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'phone', 'treatment', 'date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400

        try:
            appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400

        appointment = Appointment(
            name=data['name'].strip(),
            phone=data['phone'].strip(),
            treatment=data['treatment'].strip(),
            date=appointment_date
        )

        db.session.add(appointment)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully',
            'data': appointment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()

        if 'name' in data:
            appointment.name = data['name'].strip()
        if 'phone' in data:
            appointment.phone = data['phone'].strip()
        if 'treatment' in data:
            appointment.treatment = data['treatment'].strip()
        if 'date' in data:
            try:
                appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date format'
                }), 400
        if 'status' in data:
            appointment.status = data['status']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Appointment updated successfully',
            'data': appointment.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Appointment deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointments_bp.route('/stats', methods=['GET'])
def get_appointment_stats():
    try:
        total = Appointment.query.count()
        pending = Appointment.query.filter_by(status='pending').count()
        confirmed = Appointment.query.filter_by(status='confirmed').count()
        completed = Appointment.query.filter_by(status='completed').count()

        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'pending': pending,
                'confirmed': confirmed,
                'completed': completed
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
