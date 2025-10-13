# Primeros pasos para configurar el proyecto

## 1. Configurar Git y GitHub

1. Instala Git:
   - Windows: https://git-scm.com/download/win
   - macOS: `brew install git`
   - Linux: `sudo apt install git`
2. Configura tu usuario:
   ```bash
      git config --global user.name "Tu Nombre"
      git config --global user.email "tu@email.com"
   ```

3. Configura autenticación por SSH con GitHub:

Generar clave SSH: 
   ```bash
      ssh-keygen -t ed25519 -C "tu@email.com"
   ```

Agregar clave a [GitHub](https://docs.github.com/es/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## 2. Clonar el repositorio
   ```bash
      git clone git@github.com:raulhongo3132/administracion-de-microcreditos.git
      cd administracion-de-microcreditos
   ```

## 3. Crear y activar un entorno virtual

   ```bash
      python -m venv venv
      # Windows
      venv\Scripts\activate
      # macOS/Linux
      source venv/bin/activate
   ```

## 4. Instalar dependencias

   ```bash
      pip install -r requirements.txt
   ```
## 5. Configurar PostgreSQL y archivo .env

1. Instala PostgreSQL.
2. Crea la base de datos:
   ```bash
      CREATE DATABASE nombre_db;
      CREATE USER usuario WITH PASSWORD 'password';
      GRANT ALL PRIVILEGES ON DATABASE nombre_db TO usuario;
   ```
3. Copia .env.example como .env y ajusta las variables:
   ```bash
      FLASK_APP=app.py
      FLASK_ENV=development
      DATABASE_URL=postgresql://usuario:password@localhost/nombre_db
      SECRET_KEY=pon_aqui_una_llave_secreta
   ```
## 6. Trabajar en equipo

- Cada miembro crea su propio entorno virtual local.
- Para compartir dependencias: actualizar requirements.txt con pip freeze > requirements.txt.
- Para compartir variables de entorno sin exponer credenciales: usar .env.example.

## 7. Flujo básico con Git
   ```bash
      # Crear y cambiar a una nueva rama
      git checkout -b nombre_rama
      
      # Guardar cambios
      git add .
      git commit -m "Descripción de los cambios"
      
      # Subir rama al repositorio
      git push origin nombre_rama
      
      # Crear Pull Request en GitHub para revisión
      # Traer cambios de la rama principal
      git pull origin main
   ```
---
# `requirements.txt`
   ```bash
      Flask>=2.3.0
      psycopg2-binary>=2.9
      Flask-Migrate>=4.0
      alembic>=2.0
      Flask-WTF>=1.1
      email-validator>=2.0
      bcrypt>=4.0
      gunicorn>=21.0
      requests>=2.31
      python-dotenv>=1.0
   ```
# `.env.example`
   ```bash
      FLASK_APP=app.py
      FLASK_ENV=development
      DATABASE_URL=postgresql://usuario:password@localhost/nombre_db
      SECRET_KEY=pon_aqui_una_llave_secreta
   ```
# `.gitignore`
   ```bash
      # Entorno virtual
      venv/
      
      # Cache de Python
      pycache/
      *.pyc
      *.pyo
      
      # Variables de entorno
      .env

      # Migraciones (opcional)      
      migrations/
      
      # Archivos temporales del sistema
      .DS_Store
      Thumbs.db
   ```
# `app.py` (archivo principal de Flask)
   ```python
      from app import create_app

      app = create_app()
      
      if __name__ == "__main__":
          app.run(debug=True)

   ```




















