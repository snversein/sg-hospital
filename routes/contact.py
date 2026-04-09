from flask import Blueprint, request, jsonify
from models import db, ContactMessage

contact_bp = Blueprint('contact', __name__, url_prefix='/api/contact')

@contact_bp.route('', methods=['POST'])
def create_contact_message():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'phone', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400

        contact = ContactMessage(
            name=data['name'].strip(),
            phone=data['phone'].strip(),
            message=data['message'].strip()
        )

        db.session.add(contact)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Message sent successfully',
            'data': contact.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contact_bp.route('', methods=['GET'])
def get_contact_messages():
    try:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [msg.to_dict() for msg in messages],
            'count': len(messages)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contact_bp.route('/<int:message_id>', methods=['GET'])
def get_contact_message(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        return jsonify({
            'success': True,
            'data': message.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@contact_bp.route('/<int:message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        message.is_read = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Message marked as read',
            'data': message.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@contact_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_contact_message(message_id):
    try:
        message = ContactMessage.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Message deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
