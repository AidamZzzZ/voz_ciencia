<div align="center">
  <img src="static/img/website_UNC_logoUNC_transparente_04.png" alt="Universidad de las Ciencias" width="120" />
  <img src="static/img/ministerio-de-ciencia-y-tecnologia-vnzla-logo-png_seeklogo-480311.png" alt="MinCYT" width="120" />

  <h1>🗳️ Voz Ciencia</h1>
  <p><strong>Plataforma de Votación Electoral Institucional y Segura</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js" />
    <img src="https://img.shields.io/badge/UI-Glassmorphism-blue?style=for-the-badge" alt="Glassmorphism" />
  </p>
</div>

<br />

## 📖 Sobre el Proyecto

**Voz Ciencia** es un sistema MVP (Producto Mínimo Viable) diseñado específicamente para gestionar procesos electorales de manera digital, anónima y altamente auditable. Desarrollado con una arquitectura robusta en Django y una interfaz de usuario "Mobile-First" utilizando la estética moderna de *Glassmorphism*, el sistema garantiza una experiencia fluida e intuitiva tanto para los administradores como para los votantes.

---

## ✨ Características Principales

### 🛡️ Seguridad y Anti-Fraude
*   **Voto Anónimo y Verificable:** Cada voto genera automáticamente un comprobante criptográfico (Hash único UUID4) que se entrega al votante, garantizando el registro sin comprometer su identidad.
*   **Restricción por Dispositivo:** El sistema valida y bloquea internamente los votos duplicados, asegurando la regla estricta de *1 dispositivo = 1 voto*.
*   **Auditoría Global (System Logs):** Registro detallado de toda la actividad en la plataforma (Inicios/Cierres de sesión, Modificación de campañas, Emisión de votos). Cada acción guarda la descripción, fecha, hora y dirección IP.

### 📊 Administración y Métricas
*   **Panel de Control (Dashboard):** Gestión completa del ciclo de vida de una campaña electoral (Creación, Edición, Resultados y Eliminación).
*   **Códigos QR Dinámicos:** Generación automática de códigos QR escaneables para invitar y redireccionar a los electores directamente a la campaña específica.
*   **Estadísticas en Tiempo Real:** Integración con *Chart.js* para visualizar gráficas de dona (índice de participación basado en un censo electoral) y gráficas de barras (conteo de votos por candidato).
*   **Reportes Oficiales en PDF:** Exportación instantánea (con un solo clic) de informes ejecutivos estructurados en un diseño de formato A4, que incluyen logos institucionales (MinCYT y Universidad) adaptados perfectamente para ser impresos o archivados.

### 🎨 Diseño UI/UX
*   **Aesthetic & Glassmorphism:** Implementación de tarjetas translúcidas, desenfoques de fondo (backdrop-filter) y transiciones suaves para dar un aspecto premium y universitario.
*   **Modales Dinámicos:** Lectura cómoda de propuestas políticas mediante ventanas emergentes inteligentes que se adaptan a la pantalla y al contenido largo.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3.x, Django 5.x, SQLite (Base de datos por defecto).
*   **Frontend:** HTML5, CSS3 (Vanilla puro, Flexbox/Grid), JavaScript.
*   **Librerías Adicionales:** 
    *   `qrcode` (Generación de códigos en Python)
    *   `html2pdf.js` (Exportación de reportes PDF del lado del cliente)
    *   `Chart.js` (Visualización de datos y gráficos vectoriales)

---

## 🚀 Instalación y Despliegue Local

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd voz_ciencia
```

### 2. Crear un entorno virtual (Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

### 3. Instalar dependencias
```bash
pip install django qrcode pillow
```

### 4. Configurar la base de datos
Realiza las migraciones para estructurar el esquema interno de la aplicación.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear el superusuario (Administrador)
```bash
python manage.py createsuperuser
```
*(Ingresa tu nombre de usuario, correo electrónico y contraseña cuando se te solicite).*

### 6. Ejecutar el servidor
```bash
python manage.py runserver
```

Una vez en ejecución, la aplicación estará disponible en `http://127.0.0.1:8000`.
*   Para ingresar al panel de administración: `http://127.0.0.1:8000/admin-login/`

---

## 📂 Estructura del Código

*   `core/` - Configuraciones principales del proyecto Django y rutas base.
*   `elections/` - La aplicación central.
    *   `models.py` - Esquemas de datos (`Campana`, `Plancha`, `Votante`, `AuditoriaVoto`, `SystemLog`).
    *   `views.py` - Controladores lógicos de las vistas y procesamiento de acciones.
*   `templates/elections/` - Plantillas HTML con inyección de lógica de Django (Jinja).
*   `static/` - Archivos estáticos como logos institucionales (`img/`) y hojas de estilo globales (`css/index.css`).

---

## 🔐 Licencia y Uso

Este proyecto ha sido desarrollado como un MVP cerrado para uso institucional. Las implementaciones de seguridad son funcionales para entornos controlados, se recomienda expandir la validación de votantes mediante cruce con base de datos estudiantil en futuras iteraciones de producción.

<div align="center">
  <sub>Desarrollado con arquitectura moderna y altos estándares de UI.</sub>
</div>
