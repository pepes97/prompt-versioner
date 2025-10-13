# Flask Builder

Il modulo `prompt_versioner.app.flask_builder` fornisce la factory per creare l'applicazione web Flask.

## create_app

Funzione factory per creare e configurare l'applicazione Flask del dashboard web.

### Sintassi

```python
create_app(versioner: Any, config_name: str | None = None) -> Flask
```

**Parametri:**
- `versioner` (Any): Istanza di PromptVersioner
- `config_name` (str | None): Nome della configurazione ('development', 'production', o 'default')

**Returns:**
- `Flask`: Applicazione Flask configurata

### Configurazioni Disponibili

L'applicazione supporta diverse configurazioni:

- **`development`**: Modalità di sviluppo con debug abilitato
- **`production`**: Modalità di produzione ottimizzata
- **`default`**: Configurazione di default

La configurazione viene selezionata automaticamente dalla variabile d'ambiente `FLASK_ENV` se non specificata.

### Servizi Inizializzati

L'applicazione inizializza automaticamente i seguenti servizi:

- **`MetricsService`**: Gestione e analisi delle metriche
- **`DiffService`**: Confronto tra versioni
- **`AlertService`**: Sistema di notifiche e avvisi

### Blueprint Registrati

L'applicazione registra i seguenti blueprint:

- **`prompts_bp`**: Gestione dei prompt
- **`versions_bp`**: Gestione delle versioni
- **`alerts_bp`**: Gestione degli avvisi
- **`export_import_bp`**: Import/export dei dati

### Route Principali

#### `/` (GET)
Route principale che renderizza la dashboard.

**Returns:**
- Template `dashboard.html` con interfaccia principale

### Gestione Errori

L'applicazione include gestori per errori comuni:

#### 404 - Not Found
**Returns:**
- `{"error": "Not found"}` con status code 404

#### 500 - Internal Server Error
**Returns:**
- `{"error": "Internal server error"}` con status code 500

## Esempio di Utilizzo

### Utilizzo Base

```python
from prompt_versioner.app.flask_builder import create_app
from prompt_versioner import PromptVersioner

# Inizializza versioner
versioner = PromptVersioner("my_prompts.db")

# Crea app Flask
app = create_app(versioner, config_name="development")

# Avvia server di sviluppo
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### Utilizzo con Configurazione Personalizzata

```python
import os
from prompt_versioner.app.flask_builder import create_app
from prompt_versioner import PromptVersioner

# Configura ambiente
os.environ["FLASK_ENV"] = "production"

# Inizializza con database esistente
versioner = PromptVersioner("production_prompts.db")

# Crea app per produzione
app = create_app(versioner)

# L'app è pronta per deployment con WSGI server
```

### Accesso ai Servizi

```python
# All'interno dell'applicazione Flask, i servizi sono accessibili tramite app

@app.route("/api/custom-metrics")
def custom_metrics():
    # Accesso al MetricsService
    metrics_service = app.metrics_service
    stats = metrics_service.get_overall_stats()
    return {"stats": stats}

@app.route("/api/compare/<version_a>/<version_b>")
def compare_versions(version_a: str, version_b: str):
    # Accesso al DiffService
    diff_service = app.diff_service
    diff = diff_service.compare_versions(version_a, version_b)
    return {"diff": diff}
```

### Deployment con Gunicorn

```python
# app.py
from prompt_versioner.app.flask_builder import create_app
from prompt_versioner import PromptVersioner

# Crea app per produzione
versioner = PromptVersioner("prompts.db")
app = create_app(versioner, "production")

if __name__ == "__main__":
    app.run()
```

```bash
# Comando per avvio con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deployment con Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Esponi porta
EXPOSE 5000

# Avvia applicazione
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```python
# docker-compose.yml
version: '3.8'
services:
  prompt-versioner:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
```

## Personalizzazione

### Aggiunta di Route Personalizzate

```python
from prompt_versioner.app.flask_builder import create_app

# Crea app base
app = create_app(versioner)

# Aggiungi route personalizzate
@app.route("/api/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.route("/api/custom-dashboard")
def custom_dashboard():
    # Logica personalizzata per dashboard
    versioner = app.versioner
    prompts = versioner.list_prompts()
    return {"prompts": prompts}
```

### Middleware Personalizzato

```python
from flask import request, jsonify
import time

# Aggiungi middleware per logging delle richieste
@app.before_request
def log_request():
    request.start_time = time.time()

@app.after_request
def log_response(response):
    duration = time.time() - request.start_time
    print(f"{request.method} {request.path} - {response.status_code} ({duration:.3f}s)")
    return response
```

### Configurazione Personalizzata

```python
# custom_config.py
import os

class CustomConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    TEMPLATE_FOLDER = 'custom_templates'
    STATIC_FOLDER = 'custom_static'

    # Configurazioni personalizzate
    CUSTOM_FEATURE_ENABLED = True
    API_RATE_LIMIT = 100

# Usa configurazione personalizzata
app = create_app(versioner)
app.config.from_object(CustomConfig)
```

## Integrazione con Autenticazione

```python
from flask_login import LoginManager, login_required

# Aggiungi autenticazione
def create_authenticated_app(versioner):
    app = create_app(versioner)

    # Configura LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Proteggi route sensibili
    @app.before_request
    def require_auth():
        if request.endpoint and not request.endpoint.startswith('auth.'):
            # Richiedi autenticazione per tutte le route eccetto auth
            pass

    return app
```

## Monitoraggio e Logging

```python
import logging
from flask.logging import default_handler

def configure_logging(app):
    # Rimuovi handler default in produzione
    if app.config.get('ENV') == 'production':
        app.logger.removeHandler(default_handler)

    # Configura logging personalizzato
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

# Usa con l'app
app = create_app(versioner)
configure_logging(app)
```

## Struttura dell'Applicazione

L'applicazione Flask creata dalla factory ha la seguente struttura:

```
Flask App
├── Templates (dashboard.html, etc.)
├── Static Files (CSS, JS, images)
├── Services
│   ├── MetricsService (analisi metriche)
│   ├── DiffService (confronti versioni)
│   └── AlertService (notifiche)
├── Controllers (Blueprint)
│   ├── prompts_bp (gestione prompt)
│   ├── versions_bp (gestione versioni)
│   ├── alerts_bp (gestione avvisi)
│   └── export_import_bp (import/export)
└── Error Handlers (404, 500)
```

## Sicurezza

### Configurazione Sicura

```python
class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Sempre da variabile d'ambiente
    SESSION_COOKIE_SECURE = True  # Solo HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Proteggi da XSS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protezione CSRF

    # Configurazioni sicurezza aggiuntive
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def add_rate_limiting(app):
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Rate limit specifici per API
    @app.route("/api/metrics")
    @limiter.limit("10 per minute")
    def api_metrics():
        return app.metrics_service.get_summary()
```
