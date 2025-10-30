import random
from prompt_versioner import PromptVersioner

print("🚀 Inizializzazione PromptVersioner...")
pv = PromptVersioner("multi-model-demo")

# Salva una versione di prompt
print("\n📝 Creazione versione prompt 'text-classifier'...")
version_id = pv.save_version(
    name="text-classifier",
    system_prompt="You are an expert text classifier. Analyze the given text and provide accurate classification.",
    user_prompt="Classify the following text into one of these categories: positive, negative, neutral.\n\nText: {text}",
)

# Ottieni la versione appena creata
versions = pv.list_versions("text-classifier")
version_number = versions[0]["version"]  # L'ultima creata è la prima
print(f"✅ Versione creata: {version_number} (ID: {version_id})")

# Configurazione modelli con caratteristiche realistiche
models_config = {
    "gpt-4o": {
        "input_cost": 0.0025,
        "output_cost": 0.01,
        "avg_latency": 1234,
        "latency_variance": 300,
        "quality_base": 0.947,
        "success_rate": 0.988,
        "calls": 247,
    },
    "gpt-4o-mini": {
        "input_cost": 0.00015,
        "output_cost": 0.0006,
        "avg_latency": 487,
        "latency_variance": 150,
        "quality_base": 0.893,
        "success_rate": 0.973,
        "calls": 412,
    },
    "claude-3-5-sonnet": {
        "input_cost": 0.003,
        "output_cost": 0.015,
        "avg_latency": 1567,
        "latency_variance": 400,
        "quality_base": 0.921,
        "success_rate": 0.962,
        "calls": 183,
    },
}

print("\n🤖 Simulazione chiamate con diversi modelli...")
print("=" * 70)

total_calls = 0
for model_name, config in models_config.items():
    print(f"\n{model_name}: Logging {config['calls']} chiamate...")

    for i in range(config["calls"]):
        # Simula variazioni realistiche
        input_tokens = random.randint(80, 150)  # nosec
        output_tokens = random.randint(30, 80)  # nosec
        total_tokens = input_tokens + output_tokens

        # Calcola costo basato su token
        cost = (input_tokens * config["input_cost"] / 1000) + (
            output_tokens * config["output_cost"] / 1000
        )

        # Simula latenza con varianza
        latency = config["avg_latency"] + random.randint(
            -config["latency_variance"], config["latency_variance"]
        )  # nosec
        latency = max(100, latency)  # Non meno di 100ms

        # Simula quality score con piccole variazioni
        quality = config["quality_base"] + random.uniform(-0.05, 0.05)  # nosec
        quality = max(0, min(1, quality))  # Clamp tra 0 e 1

        # Simula successo/fallimento basato su success_rate
        success = random.random() < config["success_rate"]  # nosec

        # Log metriche
        pv.log_metrics(
            name="text-classifier",
            version=version_number,
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_eur=cost,
            latency_ms=latency,
            quality_score=quality if success else None,
            success=success,
            error_message=None if success else "Random simulated error",
        )

        total_calls += 1

        # Progress indicator
        if (i + 1) % 50 == 0:
            print(f"  ✓ {i + 1}/{config['calls']} chiamate completate")

    print(f"  ✅ {model_name}: {config['calls']} chiamate completate")

print("\n" + "=" * 70)
print(f"🎉 Demo completata! Totale chiamate simulate: {total_calls}")
print("\n📊 Ora puoi:")
print("  1. Avviare il dashboard: python -m examples.run_dashboard")
print("  2. Cliccare sul prompt 'text-classifier'")
print(f"  3. Aprire i dettagli della versione {version_number}")
print("  4. Vedere il confronto tra i 4 modelli! 🤖")
print("\n💡 Cerca i badge dorati per i modelli migliori:")
print("  ⚡ Fastest: gpt-4o-mini")
print("  💰 Cheapest: gemini-pro")
print("  ⭐ Best Quality: gpt-4o")
print("  ✅ Most Reliable: gpt-4o")
