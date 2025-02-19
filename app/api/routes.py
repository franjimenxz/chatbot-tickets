from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Chatbot de Gastos en funcionamiento 🚀"}
