# Sistema de Administración de Microcréditos

Sistema Flask para gestión de préstamos informales con cobradores.

## 🚀 Instalación Rápida

### 1. Clonar y configurar entorno
```bash
    git clone git@github.com:raulhongo3132/administracion-de-microcreditos.git
    cd administracion-de-microcreditos
    python -m venv env
    source env/bin/activate
```

### 2. Instalar dependencias
```bash
    pip install -r requirements.txt
```
### 3. Configurar base de datos PostgreSQL
En postgres crea la base de datos
```
    create database microcreditos'
```
### 4. Configurar aplicación
```bash
    # Copiar configuración ejemplo y EDITAR con tus datos
    cp config.example.py config.py
    # ⚠️ EDITAR config.py con tu SECRET_KEY y DATABASE_URL reales
```
Para la SECRET_KEY puedes hacer un:
```bash
    python -c "import secrets; print(secrets.token_urlsafe(50))"
```
### 5. Inicializar base de datos
```bash
    flask db upgrade
    python create_admin.py
```
### 6. Ejecutar aplicación
```bash
    flask run
```
## 📋 Primeros Pasos

Edita config.py con tus datos reales:

    SECRET_KEY: Genera una clave única

    SQLALCHEMY_DATABASE_URI: Tu conexión a PostgreSQL

Crea la base de datos:

```sql
    CREATE DATABASE microcreditos;
```
    Usuario por defecto:

        Usuario: admin

        Contraseña: admin123


### 3. **.gitignore** (asegúrate de incluir config.py):
```.gitignore
    # Entorno virtual
    env/
    venv/
    .env

    # Base de datos (NO subir)
    *.db
    *.sqlite3
    instance/

    # Archivos de Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    *.egg-info/
    .installed.cfg
    *.egg

    # Archivos de IDE
    .vscode/
    .idea/
    *.swp
    *.swo

    # Logs
    *.log

    # Archivos temporales
    *.tmp
    *.temp

    # Archivos de sistema
    .DS_Store
    Thumbs.db

    # Migraciones (opcional - puedes subirlas o regenerarlas)
    # migrations/
```

### 4. **Archivos que SÍ van a GitHub**:
```
microcreditos-flask/
├── .gitignore
├── requirements.txt
├── README.md
├── config.example.py ← EJEMPLO para que copien
├── create_admin.py
├── run.py
└── app/
├── init.py
├── models.py
├── forms.py
├── auth/
│ ├── routes.py
│ └── templates/
├── admin/
│ └── routes.py
├── customers/
│ └── routes.py
├── collectors/
│ └── routes.py
├── templates/
│ ├── base_auth.html
│ └── auth/
└── static/
└── css/
```

### 5. **Instrucciones para tu equipo**:

Cada miembro del equipo deberá:

1. **Clonar el repo**
2. **Crear `config.py` desde el ejemplo**:
   ```bash
   cp config.example.py config.py
   ```
3. Editar config.py con sus propias credenciales
4. Tener su propia base de datos PostgreSQL