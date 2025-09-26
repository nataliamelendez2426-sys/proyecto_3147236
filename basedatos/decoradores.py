from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
import re
from flask_mail import Message
# basedatos/extensions.py
from flask_mail import Mail

mail = Mail()


def role_required(*roles):
    """Decorador para restringir acceso según roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("⚠️ Debes iniciar sesión primero", "warning")
                return redirect(url_for('auth.login'))

            if current_user.Rol.lower() not in [r.lower() for r in roles]:
                flash("❌ No tienes permisos para acceder a esta página", "danger")
                return redirect(url_for('auth.login'))

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def validar_password(password):
    """Valida que la contraseña cumpla con las políticas de seguridad."""
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La contraseña debe contener al menos un carácter especial."
    if re.search(r"(012|123|234|345|456|567|678|789)", password):
        return "La contraseña no puede contener números consecutivos."
    return None


def validar_email(email):
    """Valida formato básico de email."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def send_reset_email(user_email, user_name, token):
    from flask import url_for
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = Message(
        subject="Restablece tu contraseña",
        recipients=[user_email],
        body=(
            f"Hola {user_name},\n\n"
            "Para restablecer tu contraseña, haz click en el siguiente enlace:\n"
            f"{reset_url}\n\n"
            "Si no solicitaste este cambio, ignora este correo."
        )
    )
    mail.send(msg)
