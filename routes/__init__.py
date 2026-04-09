from flask import Blueprint

def create_blueprints():
    from .appointments import appointments_bp
    from .contact import contact_bp
    from .chat import chat_bp
    from .admin import admin_bp
    
    return [appointments_bp, contact_bp, chat_bp, admin_bp]
