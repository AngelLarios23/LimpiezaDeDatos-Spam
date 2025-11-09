from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, batch_predict  # ← Asegúrate de importar ambos

app = FastAPI(title="SpamCleaner API")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a ["http://localhost"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenida a SpamCleaner Web"}

# Incluir ambos routers
app.include_router(predict.router, prefix="/api", tags=["Predicción"])
app.include_router(batch_predict.router, prefix="/api", tags=["Batch"])  # ← Esta línea es clave