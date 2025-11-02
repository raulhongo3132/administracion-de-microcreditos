# Importar todos los formularios para mantener compatibilidad
from app.auth.forms import (
    LoginForm, 
    PasswordRecoveryForm, 
    CodeVerificationForm, 
    ResetPasswordForm
)
from app.admin.forms import UserRegistrationForm
from app.collectors.forms import LoanForm

# También puedes re-exportar todos bajo un namespace común si lo prefieres
__all__ = [
    'LoginForm',
    'UserRegistrationForm',
    'LoanForm',
    'PasswordRecoveryForm',
    'CodeVerificationForm',
    'ResetPasswordForm'
]