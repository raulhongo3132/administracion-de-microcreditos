# 💳 Microcredit App

Aplicación web para la **gestión de microcréditos**, diseñada para que cobradores registren pagos y el administrador principal pueda consultar reportes y controlar la cartera en tiempo real.  

## 🚀 Stack Tecnológico

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask, con virtualenv)  
- **Base de Datos:** PostgreSQL  
- **Diseño UI:** Figma  

---

## 📂 Estructura del proyecto

backend/ → API REST con Flask
frontend/ → Interfaces en HTML+CSS+JS
docs/ → Documentación de negocio, arquitectura y diseño


---

## 🔧 Instalación y primeros pasos

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-org/microcredit-app.git
cd microcredit-app
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuración de variables de entorno

Crea un archivo .env en backend/ con la configuración de la BD:

```bash
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:password@localhost:5432/microcredit
SECRET_KEY=supersecreto
```

### 4. Iniciar el servidor
```bash
flask run
```
El backend estará disponible en http://localhost:5000.

### 5. Frontend
---
Abrir frontend/index.html en el navegador (o servirlo con un servidor estático).

### 📚 Documentación

📊 [Plan de Negocios](docs/business-plan.md)
📄 [Arquitectura](docs/arquitectura.md)
🎨 [Diseño UI](docs/ui-design.md)
🛠 [Guía de primeros pasos](docs/primeros_pasos.md)

---
### ✅ Roadmap
- [ ] Definición de endpoints backend
- [ ] Conexión a PostgreSQL
- [ ] Autenticación de usuarios
- [ ] Dashboards en frontend
- [ ] Reportes automáticos
- [ ] Pruebas e integración

---
### 👥 Roles

PO: Rene Bermejo

PM: Raúl Valverde

Frontend: Fernanda Iglesias / Gustavo Granados

Backend: Rebeca Gómez

DBA: Alfredo Esquivel

---
### 🤝 Contribución

Fork del repositorio

Rama de feature: git checkout -b feature/nueva-funcionalidad

Commit: git commit -m "feat: agrega nueva funcionalidad"

Push: git push origin feature/nueva-funcionalidad

Pull Request

### 📜 Licencia

MIT License. [Ver](docs/LICENSE)

## -- Notas --

- Para el PO, DBA y BE: [Link al google sheets del cliente](https://docs.google.com/spreadsheets/d/1zv5CVmtzXvHYGdaY3UP40fK2whJVYFIGNw84OHz_w0c/edit?usp=sharing).
- Lista de tareas y diagramas [Link a sheets](https://docs.google.com/spreadsheets/d/1otMOkEbiK9ZjKtjpQzz7Nzl1j3uJB0RvwW3Z7_zzNr4/edit?usp=sharing).
- Figma maquetado [Link](https://www.figma.com/design/ISTtXyQiLTXbODx6xckYG1/administracion-microcreditos?node-id=0-1&t=HzNzBObUzvOMqFpv-0)
