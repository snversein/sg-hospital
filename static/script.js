// Dr. Sushmita's Clinic - Updated JavaScript (Bootstrap Compatible)
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize Bootstrap components
let appointmentModal;
let liveToast;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap Modal and Toast
    const modalEl = document.getElementById('appointment-modal');
    if (modalEl) {
        appointmentModal = new bootstrap.Modal(modalEl);
    }
    
    const toastEl = document.getElementById('liveToast');
    if (toastEl) {
        liveToast = new bootstrap.Toast(toastEl);
    }

    initScrollAnimations();
    setMinDate();
    setupFormHandlers();
});

// Global UI Functions
function openModal() {
    if (appointmentModal) appointmentModal.show();
}

function closeModal() {
    if (appointmentModal) appointmentModal.hide();
}

function openChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) modal.classList.remove('d-none');
}

function closeChatModal() {
    const modal = document.getElementById('chat-modal');
    if (modal) modal.classList.add('d-none');
}

function showToast(message, isError = false) {
    const toastEl = document.getElementById('liveToast');
    const toastBody = document.getElementById('toast-body-text');
    if (toastEl && toastBody) {
        toastEl.className = `toast align-items-center text-white border-0 ${isError ? 'bg-danger' : 'bg-success'}`;
        toastBody.textContent = message;
        if (liveToast) liveToast.show();
    }
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => {
        observer.observe(el);
    });
}

// Set minimum date for appointment
function setMinDate() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date();
    const minDate = today.toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.setAttribute('min', minDate);
    });
}

// Form Handlers
function setupFormHandlers() {
    // Appointment Form (Modal)
    const modalForm = document.getElementById('modal-appointment-form');
    if (modalForm) {
        modalForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = {
                name: document.getElementById('apt-name').value,
                phone: document.getElementById('apt-phone').value,
                treatment: document.getElementById('apt-treatment').value,
                date: document.getElementById('apt-date').value
            };

            try {
                const response = await fetch(`${API_BASE_URL}/appointments`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    showToast('Appointment booked successfully!');
                    closeModal();
                    this.reset();
                } else {
                    showToast('Failed to book appointment.', true);
                }
            } catch (error) {
                showToast('Server error. Please try again.', true);
            }
        });
    }

    // Contact Form (Home Page)
    const contactForm = document.getElementById('appointment-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                message: document.getElementById('message').value || `Problem: ${document.getElementById('problem')?.value}`
            };

            try {
                const response = await fetch(`${API_BASE_URL}/contact`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    showToast('Message sent! We will contact you soon.');
                    this.reset();
                } else {
                    showToast('Failed to send message.', true);
                }
            } catch (error) {
                showToast('Server error. Please try again.', true);
            }
        });
    }
    
    // Chat Form
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;
            
            appendChatMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                appendChatMessage(data.reply || 'Sorry, I am having trouble connecting.', 'bot');
            } catch (error) {
                appendChatMessage('Could not reach the server.', 'bot');
            }
        });
    }
}

function appendChatMessage(content, sender) {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    
    const div = document.createElement('div');
    if (sender === 'user') {
        div.className = 'bg-primary text-white p-3 rounded-3 align-self-end shadow-sm';
        div.style.maxWidth = '85%';
    } else {
        div.className = 'bg-light text-dark p-3 rounded-3 align-self-start shadow-sm';
        div.style.maxWidth = '85%';
    }
    div.innerHTML = `<p class="small mb-0">${content}</p>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}
