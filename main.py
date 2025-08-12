from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from supabase import create_client, Client

from app.core.config import settings
from app.routes import webhook, google, calendar, categories, services, bots


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Connecting to Supabase...")
    app.state.supabase: Client = create_client(
        settings.SUPABASE_URL, settings.SUPABASE_KEY
    )
    print("✅ Supabase connected.")

    yield  # Application runs here

    print("🛑 Shutting down Supabase...")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def inject_supabase(request: Request, call_next):
    request.state.supabase = request.app.state.supabase
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])
app.include_router(google.router, prefix="/google", tags=["Google"])
app.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(bots.router, prefix="/bots", tags=["Bots"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
