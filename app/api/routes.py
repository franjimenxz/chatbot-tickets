from fastapi import APIRouter, Request, BackgroundTasks
from app.services.twilio_services import send_whatsapp_message
from app.services.ocr_services import extract_text_from_image
from app.services.expenses_services import parse_ticket_text_with_claude
from app.models.database import expenses_collection
from datetime import datetime
import re

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Recibe imágenes de WhatsApp, extrae productos y precios con Claude, y guarda en la BD.
       También permite consultar el historial de gastos agrupado por fechas."""
    form = await request.form()
    sender = form.get("From")
    message_body = form.get("Body", "").strip().lower()  # Obtener mensaje de usuario
    media_url = form.get("MediaUrl0")  # Imagen del ticket

    # ✅ Mostrar historial agrupado por fecha
    if message_body == "historial":
        user_expenses = expenses_collection.find({"usuario": sender}).sort("fecha", -1)
        user_expenses_list = list(user_expenses)  # Convertir cursor a lista

        if not user_expenses_list:
            response_message = "No tienes gastos registrados aún. 📊"
        else:
            response_message = "📜 *Historial de Gastos por Fecha:*\n"
            gastos_por_fecha = {}

            for expense in user_expenses_list:
                fecha_gasto = expense.get("fecha")  # Obtener la fecha
                if not fecha_gasto:
                    continue  # Si no hay fecha, ignorar el gasto
                
                fecha_gasto = str(fecha_gasto).split(" ")[0]  # Solo la parte de la fecha

                if fecha_gasto not in gastos_por_fecha:
                    gastos_por_fecha[fecha_gasto] = []

                for item in expense.get("items", []):
                    gastos_por_fecha[fecha_gasto].append(f"- {item['cantidad']}x {item['producto']} - ${item['precio']}")

            # Construir el mensaje agrupando por fecha
            for fecha, items in gastos_por_fecha.items():
                response_message += f"\n📅 *{fecha}:*\n" + "\n".join(items)

        background_tasks.add_task(send_whatsapp_message, sender, response_message)
        return {"status": "historial_sent"}

    # ✅ Procesar imagen del ticket
    if not media_url:
        response_message = "Por favor, envía una foto de tu ticket 🧾 o escribe 'Historial' para ver gastos organizados por fecha."
        background_tasks.add_task(send_whatsapp_message, sender, response_message)
        return {"status": "no_image"}

    # Procesar la imagen con Azure OCR
    extracted_text = extract_text_from_image(media_url)

    if not extracted_text:
        response_message = "No pude leer el ticket, intenta con otra imagen 📸"
        background_tasks.add_task(send_whatsapp_message, sender, response_message)
        return {"status": "ocr_failed"}

    # Usar Claude para interpretar el ticket correctamente
    print("Texto extraído por Azure OCR:\n", extracted_text)
    extracted_items = parse_ticket_text_with_claude(extracted_text)

    if not extracted_items:
        response_message = "Error al interpretar el ticket con IA ❌"
        background_tasks.add_task(send_whatsapp_message, sender, response_message)
        return {"status": "ai_parsing_failed"}

    # ✅ Guardar en MongoDB con la fecha actual en formato correcto
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha en formato legible
    expenses_collection.insert_one({
        "usuario": sender,
        "items": extracted_items,
        "fecha": fecha_actual  # ✅ Ahora se guarda la fecha en la BD
    })

    # Enviar respuesta en WhatsApp
    response_message = f"✅ Ticket procesado el {fecha_actual}. Productos extraídos:\n"
    for item in extracted_items:
        response_message += f"- {item['cantidad']}x {item['producto']} - ${item['precio']}\n"

    background_tasks.add_task(send_whatsapp_message, sender, response_message)

    return {"status": "success", "items": extracted_items}
