from .base import *

import os

# Detectar entorno automáticamente
# Railway, Render y otros servicios cloud suelen proveer estas variables
environment = os.getenv("DJANGO_ENV")

# Si no se especifica, detectar por otras variables
if environment is None:
    # Detectar Railway
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
        environment = "production"
    # Detectar Render
    elif os.getenv("RENDER"):
        environment = "production"
    # Detectar DATABASE_URL en producción (común en servicios cloud)
    elif os.getenv("DATABASE_URL") and not os.getenv("DATABASE_URL").startswith("postgresql://localhost"):
        environment = "production"
    else:
        environment = "development"

if environment == "production":
    from .production import *
else:
    from .development import *
