from pathlib import Path

# --- Rutas y Seguridad Básica ---
SECRET_KEY = 'clave-secreta-para-pruebas-rapidas'
DEBUG = True
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'core.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = 'static/'
USE_TZ = True 

# --- APLICACIONES INSTALADAS (CRÍTICO: Usamos rutas AppConfig) ---
INSTALLED_APPS = [
    # Aplicaciones CORE de Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    # Tus aplicaciones (REEMPLAZA NOMBRE_APLICACION_CONFIG con el nombre real en tu apps.py)
    # Por defecto, si tu app se llama 'seguridad', la clase es 'SeguridadConfig'.
    'seguridad.apps.SeguridadConfig',
    'biblio.apps.BiblioConfig',
    'catalogo.apps.CatalogoConfig',
]

# --- BASE DE DATOS PARA PRUEBAS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# --- TEMPLATES y MIDDLEWARE (Mínimo requerido) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]