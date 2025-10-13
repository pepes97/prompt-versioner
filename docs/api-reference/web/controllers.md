# Controllers

Il modulo `prompt_versioner.app.controllers` contiene i controller Flask per gestire le route API del dashboard web.

## prompts_view.py

Blueprint per le route relative ai prompt.

### prompts_bp

Blueprint Flask registrato con prefisso `/api/prompts`.

### Route

#### `GET /api/prompts`

Ottiene tutti i prompt con metadati e statistiche.

**Returns:**
- `200`: JSON con statistiche globali dei prompt
- `500`: Errore interno del server

**Risposta:**
```json
{
  "total_prompts": 10,
  "total_versions": 45,
  "total_calls": 1250,
  "avg_quality": 0.87,
  "avg_cost": 0.0023,
  "avg_latency": 350.5
}
```

**Esempio:**
```python
import requests

response = requests.get("http://localhost:5000/api/prompts")
data = response.json()
print(f"Total prompts: {data['total_prompts']}")
```

#### `GET /api/prompts/<name>/stats`

Ottiene statistiche aggregate per un prompt specifico.

**Parametri:**
- `name` (str): Nome del prompt

**Returns:**
- `200`: JSON con statistiche del prompt
- `404`: Prompt non trovato
- `500`: Errore interno del server

**Risposta:**
```json
{
  "name": "email_classifier",
  "version_count": 5,
  "total_calls": 234,
  "latest_version": "v1.2.0",
  "metrics": {
    "avg_accuracy": 0.89,
    "avg_cost": 0.0015,
    "avg_latency": 280.3
  }
}
```

**Esempio:**
```python
response = requests.get("http://localhost:5000/api/prompts/email_classifier/stats")
if response.status_code == 200:
    stats = response.json()
    print(f"Accuracy: {stats['metrics']['avg_accuracy']:.2%}")
```

#### `GET /api/prompts/<name>/ab-tests`

Ottiene versioni disponibili per A/B testing.

**Parametri:**
- `name` (str): Nome del prompt

**Returns:**
- `200`: JSON con versioni testabili
- `500`: Errore interno del server

**Criteri per A/B Testing:**
- La versione deve avere almeno `MIN_CALLS_FOR_AB_TEST` chiamate (configurabile)
- Devono essere disponibili metriche sufficienti

**Risposta:**
```json
[
  {
    "version": "v1.1.0",
    "timestamp": "2024-01-15T10:30:00Z",
    "call_count": 150,
    "avg_quality": 0.87,
    "avg_cost": 0.0020,
    "avg_latency": 320.5
  },
  {
    "version": "v1.2.0",
    "timestamp": "2024-01-20T14:15:00Z",
    "call_count": 84,
    "avg_quality": 0.91,
    "avg_cost": 0.0018,
    "avg_latency": 280.3
  }
]
```

**Esempio:**
```python
response = requests.get("http://localhost:5000/api/prompts/email_classifier/ab-tests")
versions = response.json()

for version in versions:
    print(f"Version {version['version']}: {version['call_count']} calls")
    print(f"  Quality: {version['avg_quality']:.2%}")
    print(f"  Cost: €{version['avg_cost']:.4f}")
```

#### `DELETE /api/prompts/<name>`

Elimina un prompt e tutte le sue versioni e dati correlati.

**Parametri:**
- `name` (str): Nome del prompt da eliminare

**Returns:**
- `200`: JSON con conferma di eliminazione
- `404`: Prompt non trovato
- `500`: Errore interno del server

**Risposta Successo:**
```json
{
  "success": true,
  "message": "Prompt 'email_classifier' and all its versions deleted."
}
```

**Risposta Errore:**
```json
{
  "success": false,
  "error": "Prompt not found."
}
```

**Esempio:**
```python
response = requests.delete("http://localhost:5000/api/prompts/old_prompt")
result = response.json()

if result["success"]:
    print(f"✓ {result['message']}")
else:
    print(f"✗ Error: {result['error']}")
```

## versions_view.py

Blueprint per le route relative alle versioni.

### versions_bp

Blueprint Flask registrato con prefisso `/api/versions`.

### Route Principali

#### `GET /api/versions/<prompt_name>`

Ottiene tutte le versioni per un prompt.

#### `GET /api/versions/<prompt_name>/<version>`

Ottiene dettagli di una versione specifica.

#### `POST /api/versions/<prompt_name>/compare`

Confronta due versioni di un prompt.

## alerts_view.py

Blueprint per le route relative agli avvisi.

### alerts_bp

Blueprint Flask registrato con prefisso `/api/alerts`.

### Route Principali

#### `GET /api/alerts`

Ottiene tutti gli avvisi attivi.

#### `POST /api/alerts/<alert_id>/acknowledge`

Conferma un avviso.

#### `GET /api/alerts/config`

Ottiene configurazione degli avvisi.

## export_import_view.py

Blueprint per le route di import/export.

### export_import_bp

Blueprint Flask registrato con prefisso `/api/export`.

### Route Principali

#### `GET /api/export/prompts`

Esporta tutti i prompt.

#### `POST /api/export/import`

Importa prompt da file.

## Utilizzo Completo

### Client API Completo

```python
import requests
from typing import Dict, Any, List

class PromptVersionerClient:
    """Client per API del dashboard Prompt Versioner."""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')

    def get_all_prompts(self) -> Dict[str, Any]:
        """Ottiene statistiche di tutti i prompt."""
        response = requests.get(f"{self.base_url}/api/prompts")
        response.raise_for_status()
        return response.json()

    def get_prompt_stats(self, name: str) -> Dict[str, Any]:
        """Ottiene statistiche di un prompt specifico."""
        response = requests.get(f"{self.base_url}/api/prompts/{name}/stats")
        response.raise_for_status()
        return response.json()

    def get_ab_test_versions(self, name: str) -> List[Dict[str, Any]]:
        """Ottiene versioni disponibili per A/B test."""
        response = requests.get(f"{self.base_url}/api/prompts/{name}/ab-tests")
        response.raise_for_status()
        return response.json()

    def delete_prompt(self, name: str) -> Dict[str, Any]:
        """Elimina un prompt."""
        response = requests.delete(f"{self.base_url}/api/prompts/{name}")
        response.raise_for_status()
        return response.json()

# Esempio di utilizzo
client = PromptVersionerClient("http://localhost:5000")

# Ottieni overview
overview = client.get_all_prompts()
print(f"Prompts totali: {overview['total_prompts']}")

# Analizza prompt specifico
stats = client.get_prompt_stats("email_classifier")
print(f"Versioni: {stats['version_count']}")
print(f"Chiamate totali: {stats['total_calls']}")

# Controlla versioni per A/B test
ab_versions = client.get_ab_test_versions("email_classifier")
if len(ab_versions) >= 2:
    print("✓ Pronto per A/B testing")
    for v in ab_versions:
        print(f"  {v['version']}: {v['call_count']} calls")
else:
    print("⚠️  Servono più versioni per A/B testing")
```

### Dashboard Monitoring

```python
import time
from datetime import datetime

def monitor_dashboard(client: PromptVersionerClient, interval: int = 60):
    """Monitora lo stato del dashboard."""

    while True:
        try:
            # Ottieni statistiche globali
            stats = client.get_all_prompts()
            timestamp = datetime.now().strftime("%H:%M:%S")

            print(f"\n[{timestamp}] Dashboard Status:")
            print(f"  Prompts: {stats['total_prompts']}")
            print(f"  Versions: {stats['total_versions']}")
            print(f"  Total calls: {stats['total_calls']}")
            print(f"  Avg quality: {stats['avg_quality']:.2%}")
            print(f"  Avg cost: €{stats['avg_cost']:.4f}")
            print(f"  Avg latency: {stats['avg_latency']:.1f}ms")

            # Controlla se ci sono problemi
            if stats['avg_quality'] < 0.8:
                print("  ⚠️  Quality sotto soglia!")
            if stats['avg_latency'] > 1000:
                print("  ⚠️  Latenza alta!")

        except Exception as e:
            print(f"❌ Errore monitoring: {e}")

        time.sleep(interval)

# Avvia monitoring
# monitor_dashboard(client, interval=30)
```

### Gestione Errori

```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper per chiamate API sicure."""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.ConnectionError:
        print("❌ Impossibile connettersi al server")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Risorsa non trovata")
        elif e.response.status_code == 500:
            print("❌ Errore interno del server")
        else:
            print(f"❌ Errore HTTP: {e.response.status_code}")
        return None
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return None

# Utilizzo sicuro
stats = safe_api_call(client.get_prompt_stats, "nonexistent_prompt")
if stats:
    print("Stats ottenute con successo")
else:
    print("Impossibile ottenere stats")
```

## Configurazione

### Configurazione Minima per A/B Testing

```python
# config.py
class Config:
    MIN_CALLS_FOR_AB_TEST = 30  # Minimo 30 chiamate per A/B test
    MAX_AB_TEST_VERSIONS = 10   # Massimo 10 versioni in lista
    CACHE_TIMEOUT = 300         # Cache risultati per 5 minuti
```

### Middleware per Logging

```python
from flask import request
import logging

@prompts_bp.before_request
def log_prompt_request():
    """Log delle richieste ai prompt."""
    logging.info(f"Prompt API: {request.method} {request.path}")

@prompts_bp.after_request
def log_prompt_response(response):
    """Log delle risposte ai prompt."""
    logging.info(f"Prompt API Response: {response.status_code}")
    return response
```

### Rate Limiting

```python
from flask_limiter import Limiter

# Applica rate limiting ai prompt API
@prompts_bp.route("", methods=["GET"])
@limiter.limit("100 per hour")  # Max 100 richieste/ora
def get_prompts():
    # ... logica esistente
```
