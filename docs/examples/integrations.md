# Integrations

Learn how to integrate **Prompt Versioner** with popular tools and frameworks.

## 🔗 LLM Framework Integrations

### OpenAI Integration

```python
import openai
from prompt_versioner import PromptVersioner
import time

class OpenAIIntegration:
    """Integration with OpenAI API"""

    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.pv = PromptVersioner(project_name="openai-integration")

    def call_with_tracking(self, prompt_name, version, user_input, **kwargs):
        """Call OpenAI API with automatic metrics tracking"""

        # Get prompt version
        prompt_data = self.pv.get_version(prompt_name, version)
        if not prompt_data:
            raise ValueError(f"Prompt {prompt_name} v{version} not found")

        # Prepare messages
        messages = [
            {"role": "system", "content": prompt_data["system_prompt"]},
            {"role": "user", "content": prompt_data["user_prompt"].format(input=user_input)}
        ]

        # Make API call with timing
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", "gpt-4o-mini"),
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000)
            )

            end_time = time.time()

            # Calculate metrics
            latency_ms = (end_time - start_time) * 1000
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost_eur = self.calculate_cost(response.usage, response.model)

            # Log metrics
            self.pv.log_metrics(
                name=prompt_name,
                version=version,
                model_name=response.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                cost_eur=cost_eur,
                success=True,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                metadata={
                    "user_input": user_input[:100],  # First 100 chars
                    "finish_reason": response.choices[0].finish_reason
                }
            )

            return {
                "content": response.choices[0].message.content,
                "usage": response.usage,
                "model": response.model,
                "latency_ms": latency_ms
            }

        except Exception as e:
            end_time = time.time()

            # Log error
            self.pv.log_metrics(
                name=prompt_name,
                version=version,
                latency_ms=(end_time - start_time) * 1000,
                success=False,
                error_message=str(e),
                metadata={"user_input": user_input[:100]}
            )

            raise

    def calculate_cost(self, usage, model):
        """Calculate cost in EUR based on token usage"""

        # Example pricing (update with current rates)
        pricing = {
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},  # per 1K tokens
            "gpt-4o": {"input": 0.0025, "output": 0.01},
        }

        model_pricing = pricing.get(model, pricing["gpt-4o-mini"])

        input_cost = (usage.prompt_tokens / 1000) * model_pricing["input"]
        output_cost = (usage.completion_tokens / 1000) * model_pricing["output"]

        return (input_cost + output_cost) * 0.85  # Convert USD to EUR (approximate)

# Usage
openai_integration = OpenAIIntegration(api_key="your-api-key")

# Save a prompt version
openai_integration.pv.save_version(
    name="code_assistant",
    system_prompt="You are a helpful Python programming assistant.",
    user_prompt="Help me with this Python question: {input}",
    bump_type=VersionBump.MAJOR
)

# Use with automatic tracking
result = openai_integration.call_with_tracking(
    prompt_name="code_assistant",
    version="1.0.0",
    user_input="How do I create a list comprehension?",
    model="gpt-4o-mini",
    temperature=0.3
)

print(f"Response: {result['content']}")
print(f"Latency: {result['latency_ms']:.1f}ms")
```

### LangChain Integration

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import BaseCallbackHandler
from prompt_versioner import PromptVersioner

class PromptVersionerCallback(BaseCallbackHandler):
    """LangChain callback for Prompt Versioner integration"""

    def __init__(self, pv, prompt_name, version):
        self.pv = pv
        self.prompt_name = prompt_name
        self.version = version
        self.start_time = None
        self.tokens_used = {}

    def on_llm_start(self, serialized, prompts, **kwargs):
        """Called when LLM starts running"""
        self.start_time = time.time()

    def on_llm_end(self, response, **kwargs):
        """Called when LLM ends running"""

        if self.start_time:
            latency_ms = (time.time() - self.start_time) * 1000

            # Extract token usage if available
            token_usage = response.llm_output.get('token_usage', {}) if response.llm_output else {}

            self.pv.log_metrics(
                name=self.prompt_name,
                version=self.version,
                input_tokens=token_usage.get('prompt_tokens', 0),
                output_tokens=token_usage.get('completion_tokens', 0),
                latency_ms=latency_ms,
                success=True,
                metadata={
                    "langchain_integration": True,
                    "response_generations": len(response.generations)
                }
            )

    def on_llm_error(self, error, **kwargs):
        """Called when LLM encounters an error"""

        if self.start_time:
            latency_ms = (time.time() - self.start_time) * 1000

            self.pv.log_metrics(
                name=self.prompt_name,
                version=self.version,
                latency_ms=latency_ms,
                success=False,
                error_message=str(error),
                metadata={"langchain_integration": True}
            )

class LangChainIntegration:
    """Integration with LangChain framework"""

    def __init__(self):
        self.pv = PromptVersioner(project_name="langchain-integration")

    def create_versioned_chain(self, prompt_name, version, llm):
        """Create LangChain chain with versioned prompts"""

        # Get prompt version
        prompt_data = self.pv.get_version(prompt_name, version)
        if not prompt_data:
            raise ValueError(f"Prompt {prompt_name} v{version} not found")

        # Create LangChain prompt template
        full_prompt = f"{prompt_data['system_prompt']}\n\n{prompt_data['user_prompt']}"
        prompt_template = PromptTemplate.from_template(full_prompt)

        # Create callback for tracking
        callback = PromptVersionerCallback(self.pv, prompt_name, version)

        # Create chain with callback
        chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            callbacks=[callback]
        )

        return chain

# Usage
from langchain.llms import OpenAI

integration = LangChainIntegration()

# Save versioned prompt
integration.pv.save_version(
    name="langchain_assistant",
    system_prompt="You are a helpful assistant that explains complex topics simply.",
    user_prompt="Explain {topic} in simple terms that a beginner can understand.",
    bump_type=VersionBump.MAJOR
)

# Create versioned chain
llm = OpenAI(temperature=0.7)
chain = integration.create_versioned_chain("langchain_assistant", "1.0.0", llm)

# Use chain (automatically tracks metrics)
result = chain.run(topic="machine learning")
print(result)
```

## 📊 Monitoring and Observability

### Weights & Biases Integration

```python
import wandb
from prompt_versioner import PromptVersioner

class WandbIntegration:
    """Integration with Weights & Biases for experiment tracking"""

    def __init__(self, project_name, entity=None):
        self.pv = PromptVersioner(project_name=f"wandb_{project_name}")
        self.project_name = project_name
        self.entity = entity
        self.run = None

    def start_experiment(self, experiment_name, prompt_name, version):
        """Start W&B experiment with prompt version"""

        prompt_data = self.pv.get_version(prompt_name, version)

        self.run = wandb.init(
            project=self.project_name,
            entity=self.entity,
            name=experiment_name,
            config={
                "prompt_name": prompt_name,
                "prompt_version": version,
                "system_prompt": prompt_data["system_prompt"],
                "user_prompt": prompt_data["user_prompt"],
                "prompt_metadata": prompt_data.get("metadata", {})
            }
        )

        return self.run

    def log_prompt_metrics(self, prompt_name, version, metrics):
        """Log prompt metrics to W&B"""

        if not self.run:
            raise ValueError("No active W&B run. Call start_experiment first.")

        # Log to both W&B and Prompt Versioner
        wandb.log(metrics)

        self.pv.log_metrics(
            name=prompt_name,
            version=version,
            **metrics,
            metadata={"wandb_run_id": self.run.id}
        )

    def finish_experiment(self):
        """Finish W&B experiment"""
        if self.run:
            wandb.finish()
            self.run = None

# Usage
wandb_integration = WandbIntegration("prompt-experiments")

# Start experiment
run = wandb_integration.start_experiment(
    "customer-service-v2",
    "customer_service",
    "2.1.0"
)

# Log metrics during experiment
for i in range(10):
    metrics = {
        "quality_score": 0.85 + random.uniform(-0.05, 0.05),
        "latency_ms": 400 + random.uniform(-50, 50),
        "cost_eur": 0.003 + random.uniform(-0.0005, 0.0005)
    }

    wandb_integration.log_prompt_metrics(
        "customer_service",
        "2.1.0",
        metrics
    )

wandb_integration.finish_experiment()
```

### MLflow Integration

```python
import mlflow
import mlflow.sklearn
from prompt_versioner import PromptVersioner

class MLflowIntegration:
    """Integration with MLflow for model and prompt tracking"""

    def __init__(self, tracking_uri=None, experiment_name="prompt-versioning"):
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

        mlflow.set_experiment(experiment_name)
        self.pv = PromptVersioner(project_name="mlflow_integration")

    def log_prompt_as_artifact(self, prompt_name, version):
        """Log prompt version as MLflow artifact"""

        prompt_data = self.pv.get_version(prompt_name, version)

        with mlflow.start_run():
            # Log prompt content as parameters
            mlflow.log_param("prompt_name", prompt_name)
            mlflow.log_param("prompt_version", version)
            mlflow.log_param("system_prompt_hash", hash(prompt_data["system_prompt"]))
            mlflow.log_param("user_prompt_hash", hash(prompt_data["user_prompt"]))

            # Create temporary files for artifacts
            import tempfile
            import json

            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(prompt_data, f, indent=2)
                mlflow.log_artifact(f.name, "prompts")

            return mlflow.active_run().info.run_id

    def log_prompt_metrics_to_mlflow(self, prompt_name, version, metrics):
        """Log prompt performance metrics to MLflow"""

        with mlflow.start_run():
            # Log metrics to MLflow
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    mlflow.log_metric(key, value)

            # Also log to Prompt Versioner
            self.pv.log_metrics(
                name=prompt_name,
                version=version,
                **metrics,
                metadata={"mlflow_run_id": mlflow.active_run().info.run_id}
            )

# Usage
mlflow_integration = MLflowIntegration()

# Log prompt as artifact
run_id = mlflow_integration.log_prompt_as_artifact("code_assistant", "1.2.0")
print(f"Logged prompt to MLflow run: {run_id}")

# Log performance metrics
mlflow_integration.log_prompt_metrics_to_mlflow(
    "code_assistant",
    "1.2.0",
    {
        "accuracy": 0.92,
        "f1_score": 0.89,
        "precision": 0.91,
        "recall": 0.87
    }
)
```

## 🗄️ Database Integrations

### PostgreSQL Integration

```python
import psycopg2
from prompt_versioner import PromptVersioner

class PostgreSQLIntegration:
    """Integration with PostgreSQL for external metrics storage"""

    def __init__(self, connection_params):
        self.pv = PromptVersioner(project_name="postgres_integration")
        self.conn = psycopg2.connect(**connection_params)
        self.setup_tables()

    def setup_tables(self):
        """Create tables for storing prompt metrics"""

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS prompt_metrics_external (
                    id SERIAL PRIMARY KEY,
                    prompt_name VARCHAR(255) NOT NULL,
                    version VARCHAR(50) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    model_name VARCHAR(100),
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    latency_ms FLOAT,
                    quality_score FLOAT,
                    cost_eur FLOAT,
                    success BOOLEAN,
                    metadata JSONB
                )
            """)
            self.conn.commit()

    def log_metrics_dual(self, prompt_name, version, **metrics):
        """Log metrics to both Prompt Versioner and PostgreSQL"""

        # Log to Prompt Versioner
        self.pv.log_metrics(
            name=prompt_name,
            version=version,
            **metrics
        )

        # Log to PostgreSQL
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO prompt_metrics_external
                (prompt_name, version, model_name, input_tokens, output_tokens,
                 latency_ms, quality_score, cost_eur, success, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                prompt_name,
                version,
                metrics.get("model_name"),
                metrics.get("input_tokens"),
                metrics.get("output_tokens"),
                metrics.get("latency_ms"),
                metrics.get("quality_score"),
                metrics.get("cost_eur"),
                metrics.get("success", True),
                json.dumps(metrics.get("metadata", {}))
            ))
            self.conn.commit()

    def get_aggregated_metrics(self, prompt_name, version, days=7):
        """Get aggregated metrics from PostgreSQL"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) as total_calls,
                    AVG(quality_score) as avg_quality,
                    AVG(latency_ms) as avg_latency,
                    SUM(cost_eur) as total_cost,
                    SUM(CASE WHEN success THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as success_rate
                FROM prompt_metrics_external
                WHERE prompt_name = %s AND version = %s
                AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '%s days'
            """, (prompt_name, version, days))

            result = cur.fetchone()

            return {
                "total_calls": result[0],
                "avg_quality": float(result[1]) if result[1] else 0,
                "avg_latency": float(result[2]) if result[2] else 0,
                "total_cost": float(result[3]) if result[3] else 0,
                "success_rate": float(result[4]) if result[4] else 0
            }

# Usage
postgres_integration = PostgreSQLIntegration({
    "host": "localhost",
    "database": "prompt_metrics",
    "user": "your_user",
    "password": "your_password"
})

# Log metrics to both systems
postgres_integration.log_metrics_dual(
    "customer_service",
    "2.1.0",
    model_name="gpt-4o",
    input_tokens=150,
    output_tokens=200,
    latency_ms=420,
    quality_score=0.91,
    cost_eur=0.0035,
    success=True
)

# Get aggregated metrics
metrics = postgres_integration.get_aggregated_metrics("customer_service", "2.1.0")
print(f"Total calls: {metrics['total_calls']}")
print(f"Average quality: {metrics['avg_quality']:.2f}")
```

## 📚 Next Steps

- [Advanced Workflows](advanced-workflows.md) - Complex deployment patterns
- [Best Practices](best-practices.md) - Comprehensive guidelines
- [Performance Monitoring](../user-guide/performance-monitoring.md) - Monitor your integrations
