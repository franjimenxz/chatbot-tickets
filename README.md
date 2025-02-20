# Chatbot de Análisis de Gastos a partir de Tickets de Compra

## Descripción
Este chatbot permite a los usuarios enviar una foto de un ticket de compra a través de WhatsApp. El sistema extrae automáticamente la cantidad, el producto y el precio de cada artículo y los almacena en una base de datos. Además, los usuarios pueden solicitar el historial de compras y recibir un resumen dividido por fecha.

## Tecnologías Utilizadas
- **FastAPI** → Framework backend para la API.
- **Ngrok** → Para exponer la API localmente durante pruebas.
- **Azure Vision Studio** → Para detectar y extraer el texto de la imagen del ticket.
- **IA de Claude** → Para filtrar y estructurar la información en cantidad, producto y precio.
- **MongoDB** → Para almacenar los datos extraídos.
- **Twilio API (Sandbox for WhatsApp)** → Para recibir imágenes y responder mensajes.

## Funcionalidades
### 📌 Extracción de Datos desde un Ticket
- El usuario envía una imagen de un ticket por WhatsApp.
- **Azure Vision Studio** detecta y extrae el texto.
- **Claude AI** procesa el texto y extrae la cantidad, el producto y el precio.
- Los datos se almacenan en **MongoDB** junto con la fecha de compra.

### 📌 Consultar Historial de Compras
- El usuario puede solicitar su historial escribiendo **"Mis compras"**.
- El chatbot responde con los gastos organizados por fecha.

### 📌 Clasificación de Gastos por Categoría
- Cada compra se clasifica automáticamente en categorías como **Restaurante, Supermercado, Entretenimiento**.
- Se puede solicitar el total gastado por categoría con el comando **"Mis gastos en [categoría]"**.

## Instalación y Configuración
### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/franjimenxz/chatbot-tickets.git
cd chatbot-tickets
```

### 2️⃣ Crear y Activar un Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno
Crear un archivo `.env` con:
```ini
MONGO_URI=mongodb://localhost:27017/chatbot
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_MY_NUMBER=whatsapp:+your_phone_number
AZURE_VISION_KEY=your_azure_key
AZURE_VISION_ENDPOINT=your_azure_endpoint
```

### 5️⃣ Ejecutar el Servidor FastAPI
```bash
uvicorn app.main:app --reload
```

### 6️⃣ Exponer la API con Ngrok
```bash
ngrok http 8000
```
Configurar la URL en Twilio como webhook para WhatsApp.

## Uso del Chatbot
### 📩 Enviar un Ticket
1. **Mandar una foto de un ticket** al número de WhatsApp configurado.
2. El bot extraerá los datos y los guardará.

### 📊 Consultar Historial
- **"Mis compras"** → Muestra todas las compras organizadas por fecha.
- **"Mis gastos en [categoría]"** → Muestra el total gastado en una categoría específica.

## Próximos Pasos
- Mejorar la detección de productos con modelos personalizados.
- Agregar alertas de ahorro y comparación de precios.
- Integrar reportes en formato PDF o gráficos de gasto.

🚀 **Este chatbot facilita la gestión de gastos automatizando la lectura y análisis de tickets de compra.**

