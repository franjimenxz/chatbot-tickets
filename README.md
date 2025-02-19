# Chatbot de Análisis de Gastos a partir de Tickets de Compra

## Descripción

Este chatbot permite a los usuarios enviar una imagen de un ticket de compra a través de WhatsApp. Luego, el sistema extrae información sobre los productos comprados, las cantidades y los precios, almacena estos datos y permite llevar un control de los gastos.

## Características Principales

- Recibe una imagen de un ticket de compra por WhatsApp.
- Extrae información relevante: **producto, cantidad y precio**.
- Almacena los datos en una base de datos.
- Permite consultar el historial de gastos.

## Tecnologías Utilizadas

- **Backend:** FastAPI
- **Procesamiento de Imágenes (OCR):** Tesseract OCR
- **Base de Datos:** MongoDB
- **Integración con WhatsApp:** Twilio Sandbox para WhatsApp
- **Hosting:** VPS gratuito Railway

## Arquitectura del Sistema

1. **Recepción de Imagen**: El usuario envía una foto del ticket de compra a WhatsApp.
2. **Extracción de Texto (OCR)**: Se usa Tesseract OCR para convertir la imagen en texto.
3. **Procesamiento de Datos**: Se filtra la información para identificar productos, cantidades y precios.
4. **Almacenamiento en Base de Datos**: Se guarda la información en MongoDB o PostgreSQL.
5. **Consulta de Historial**: Se puede acceder a los datos almacenados para revisar los gastos.

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/franjimenxz/chatbot-tickets.git
cd chatbot-tickets
```

### 2. Crear y Activar un Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

#### Linux (Debian/Ubuntu)

```bash
sudo apt install tesseract-ocr
```

#### Windows

1. Descargar desde [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
2. Agregar Tesseract a la variable de entorno `PATH`.

### 5. Configurar Twilio para WhatsApp

1. Crear una cuenta en [Twilio](https://www.twilio.com/try-twilio).
2. Activar **Twilio Sandbox for WhatsApp**.
3. Obtener credenciales (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`).
4. Configurar un webhook que apunte a nuestro backend.

### 6. Configurar Base de Datos

#### Opción 1: MongoDB

```bash
sudo systemctl start mongod  # Iniciar MongoDB
```

#### Opción 2: PostgreSQL

```bash
sudo systemctl start postgresql  # Iniciar PostgreSQL
```

### 7. Ejecutar el Backend

```bash
python app.py  # Flask
# O
uvicorn app:app --reload  # FastAPI
```

### 8. Probar el Chatbot

1. Enviar una imagen de un ticket al bot de WhatsApp.
2. Verificar que los productos, cantidades y precios sean extraídos correctamente.
3. Consultar los gastos almacenados en la base de datos.

## Próximos Pasos (Versiones Futuras)

- Mejorar el procesamiento de datos con Machine Learning.
- Generar reportes automáticos de gastos excesivos.
- Implementar alertas personalizadas sobre hábitos de compra.

---

Este proyecto busca ser una herramienta sencilla y efectiva para el control de gastos personales a partir de tickets de compra. 🚀

