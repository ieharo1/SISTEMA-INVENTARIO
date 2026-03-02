# Sistema de Inventario - FastAPI

Sistema de gestión de inventario con FastAPI, MongoDB y Bootstrap 5.

---

## 📝 Descripción

API RESTful para gestión de inventario con autenticación JWT, permitiendo gestionar productos, proveedores y movimientos de inventario.

---

## 🏗 Estructura

```
curso_platzi/
├── app/
│   ├── config.py              # Configuración
│   ├── database.py            # Conexión MongoDB
│   ├── main.py                # Aplicación FastAPI
│   ├── schemas/
│   │   └── schemas.py         # Modelos Pydantic
│   ├── services/
│   │   └── auth_service.py    # Autenticación JWT
│   ├── repositories/
│   │   └── repository.py      # CRUD operations
│   ├── routes/
│   │   ├── auth.py            # Rutas de autenticación
│   │   └── inventory.py       # Rutas de inventario
│   └── templates/             # Plantillas HTML
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── dashboard.html
│       ├── products.html
│       ├── suppliers.html
│       └── movements.html
├── requirements.txt
└── README.md
```

---

## 💻 Requisitos

- Python 3.8+
- MongoDB
- Node.js (opcional)

---

## 🚀 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/ieharo1/curso_platzi.git
   cd curso_platzi
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar MongoDB:**
   - Asegúrate de tener MongoDB ejecutándose en `localhost:27017`
   - O modifica la URL en `app/config.py`

5. **Ejecutar el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Acceder a la aplicación:**
   - Abre `http://localhost:8000` en tu navegador

---

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI, Python 3.8+
- **Base de datos:** MongoDB con Motor
- **Frontend:** Bootstrap 5, Jinja2
- **Autenticación:** JWT
- **Validación:** Pydantic

---

## 📦 Colecciones MongoDB

- `users` - Usuarios del sistema
- `products` - Catálogo de productos
- `suppliers` - Proveedores
- `inventory_movements` - Movimientos de inventario

---

## ✨ Características

- Login/Registro con JWT
- CRUD completo de productos
- Gestión de proveedores
- Registro de movimientos (entradas/salidas)
- Dashboard con métricas
- Alertas de stock mínimo

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack · Automatización · Data**

- 📧 Email: zackharo1@gmail.com
- 📱 WhatsApp: 098805517
- 💻 GitHub: https://github.com/ieharo1
- 🌐 Portafolio: https://ieharo1.github.io/portafolio-isaac.haro/

---

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.
