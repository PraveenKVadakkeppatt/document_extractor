from app.router.upload import router as upload_router
from app.router.status import router as status_router
from app.router.export import router as export_router
from fastapi import FastAPI
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Document Extractor API")


# routers
app.include_router(upload_router)
app.include_router(status_router)
app.include_router(export_router)


@app.get('/')
async def home():
    return {"message": "Document Extractor Running"} 