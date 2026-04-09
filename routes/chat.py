from flask import Blueprint, request, jsonify
import os
from groq import Groq

chat_bp = Blueprint('chat', __name__)

system_prompt = """You are Dr. Sushmita's Ayurvedic Health Assistant. You help visitors with information about:

1. Treatments & Therapies:
   - Panchakarma (Detoxification therapies like Vamana, Virechana)
   - Kati Basti, Janu Basti, Greeva Basti (Localized oil therapies)
   - Cupping Therapy (Hot/Fire Cupping)
   - Leech Therapy (Raktamokshan)
   - Abhyanga (Full body massage)
   - Shirodhara, Nasya, Netra Tarpan
   - Acupuncture Needling, Agnikarma

2. Conditions We Treat:
   - Slip Disc, Sciatica, Frozen Shoulder
   - Cervical & Lumbar Spondylosis
   - Knee Pain, Arthritis, Back Pain, Neck Pain
   - Migraine, Joint Pain
   - Tennis Elbow, Carpal Tunnel
   - Paralysis, PCOD/PCOS

3. Clinic Information:
   - Location: 4th Floor, Arcade Complex, Shiv Talkies Chowk, Bilaspur (C.G.)
   - Phone: +91 9755550613
   - Timings: 09:00 AM - 08:00 PM
   - Doctor: Dr. Sushmita Gumber (B.A.M.S., Neurotherapy Specialist)

4. Wellness Programs:
   - Detoxification & Purification
   - Skin & Hair Care (Soundarya Vardhani)
   - Stress & Mental Well-being (Manas Mitra)
   - Post-Natal Care (Matra Raksha)
   - Pregnancy Care (Garbh Sanskar)
   - Neuro & Spine Care (Vata Chikitsa)

Be helpful, concise, and professional. If asked about specific medical advice, recommend booking an appointment."""

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'Chat service not configured'}), 500
        
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        reply = response.choices[0].message.content
        return jsonify({'reply': reply})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
