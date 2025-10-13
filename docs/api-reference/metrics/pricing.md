# Pricing

The `prompt_versioner.metrics.pricing` module manages model pricing and calculates LLM call costs.

## ModelPricing

Class representing pricing information for a specific model.

### Constructor

```python
def __init__(self, input_price: float, output_price: float, currency: str = "EUR")
```

**Parameters:**
- `input_price` (float): Price per 1M input tokens
- `output_price` (float): Price per 1M output tokens
- `currency` (str): Currency code (default: "EUR")

### Methods

#### calculate_cost()

```python
def calculate_cost(self, input_tokens: int, output_tokens: int) -> float
```

Calculates the cost for a specific token usage.

**Parameters:**
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens

**Returns:**
- `float`: Total cost in the specified currency

**Example:**
```python
from prompt_versioner.metrics.pricing import ModelPricing

# Define pricing for GPT-4
gpt4_pricing = ModelPricing(
    input_price=0.92,   # €0.92 per 1M input tokens
    output_price=3.68   # €3.68 per 1M output tokens
)

# Calculate cost for a call
cost = gpt4_pricing.calculate_cost(input_tokens=1000, output_tokens=500)
print(f"Cost: €{cost:.6f}")  # €0.002760
```

#### to_dict()

```python
def to_dict(self) -> Dict[str, float | str]
```

Converts the object to a dictionary.

**Returns:**
- `Dict[str, float | str]`: Dictionary representation

## PricingManager

Class for managing pricing of multiple models and calculating costs.

### Constructor

```python
def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None)
```

**Parameters:**
- `custom_pricing` (Optional[Dict]): Custom prices to override defaults

### Default Prices

The manager includes up-to-date prices for major LLM models:

```python
DEFAULT_MODEL_PRICING = {
    # Claude models (Anthropic)
    "claude-opus-4-1": {"input": 13.80, "output": 69.00},
    "claude-sonnet-4-5": {"input": 5.06, "output": 23.00},
    "claude-haiku-4": {"input": 0.92, "output": 4.60},
    # Mistral models
    "mistral-large-24-11": {"input": 1.84, "output": 5.52},
    "mistral-medium-3": {"input": 0.37, "output": 1.84},
    "mistral-small-3-1": {"input": 0.09, "output": 0.28},
    # OpenAI models
    "gpt-5": {"input": 1.15, "output": 9.20},
    "gpt-4-1": {"input": 0.92, "output": 3.68},
    "gpt-4o": {"input": 1.15, "output": 4.60},
    "gpt-4o-mini": {"input": 0.18, "output": 0.73},
}
```

### Methods

#### get_pricing()

```python
def get_pricing(self, model_name: str) -> Optional[ModelPricing]
```

Gets pricing information for a model.

**Parameters:**
- `model_name` (str): Model name

**Returns:**
- `Optional[ModelPricing]`: ModelPricing object or None if not found

#### add_model()

```python
def add_model(self, model_name: str, input_price: float, output_price: float) -> None
```

Adds or updates pricing for a model.

**Parameters:**
- `model_name` (str): Model name
- `input_price` (float): Price per 1M input tokens
- `output_price` (float): Price per 1M output tokens

#### remove_model()

```python
def remove_model(self, model_name: str) -> bool
```

Removes a model from pricing.

**Parameters:**
- `model_name` (str): Model name

**Returns:**
- `bool`: True if removed, False if not found

#### list_models()

```python
def list_models(self) -> list[str]
```

Gets the list of all models with pricing.

**Returns:**
- `List[str]`: List of model names

**Example:**
```python
from prompt_versioner.metrics.pricing import PricingManager

# Create manager with custom pricing
custom_pricing = {
    "custom-model": {"input": 0.5, "output": 1.0}
}
manager = PricingManager(custom_pricing)

# Add a new model
manager.add_model("my-model", input_price=0.3, output_price=0.8)

# List all models
models = manager.list_models()
print(f"Available models: {len(models)}")
for model in sorted(models):
    pricing = manager.get_pricing(model)
    if pricing:
        print(f"  {model}: €{pricing.input_price}/€{pricing.output_price}")
```

#### calculate_cost()

```python
def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float
```

Calculates the cost for a model call.

**Parameters:**
- `model_name` (str): Model name
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens

**Returns:**
- `float`: Cost in EUR (0.0 if model not found)

**Example:**
```python
manager = PricingManager()

# Calculate costs for different models
models_to_test = ["gpt-4o", "gpt-4o-mini", "claude-haiku-4"]
input_tokens, output_tokens = 1000, 500

print("Cost comparison:")
for model in models_to_test:
    cost = manager.calculate_cost(model, input_tokens, output_tokens)
    print(f"  {model}: €{cost:.6f}")
```

#### estimate_cost()

```python
def estimate_cost(
        self, model_name: str, input_tokens: int, output_tokens: int, num_calls: int = 1
    ) -> Dict[str, float]
```
Estimates costs for multiple calls.

**Parameters:**
- `model_name` (str): Model name
- `input_tokens` (int): Input tokens per call
- `output_tokens` (int): Output tokens per call
- `num_calls` (int): Number of calls (default: 1)

**Returns:**
- `Dict[str, float]`: Dictionary with cost breakdown

**Example:**
```python
# Estimate costs for a batch of calls
estimate = manager.estimate_cost(
    model_name="gpt-4o",
    input_tokens=500,
    output_tokens=200,
    num_calls=1000
)

print(f"Estimate for 1000 calls:")
print(f"  Cost per call: €{estimate['cost_per_call']:.6f}")
print(f"  Total cost: €{estimate['total_cost']:.2f}")
print(f"  Total input tokens: {estimate['total_input_tokens']:,}")
print(f"  Total output tokens: {estimate['total_output_tokens']:,}")
```

#### compare_models()

```python
def compare_models(self, input_tokens: int, output_tokens: int) -> Dict[str, float]
```

Compares costs across all models.

**Parameters:**
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens

**Returns:**
- `Dict[str, float]`: Dictionary model -> cost, sorted by ascending cost

#### get_cheapest_model()

```python
def get_cheapest_model(self, input_tokens: int, output_tokens: int) -> tuple[str, float]:
```

Finds the cheapest model for a given usage.

**Parameters:**
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens

**Returns:**
- `tuple[str, float]`: Tuple (model_name, cost)

**Example:**
```python
# Compare all models
costs = manager.compare_models(input_tokens=2000, output_tokens=1000)

print("Cost ranking (cheapest first):")
for i, (model, cost) in enumerate(costs.items(), 1):
    print(f"  {i}. {model}: €{cost:.6f}")

# Find the cheapest
cheapest_model, cheapest_cost = manager.get_cheapest_model(2000, 1000)
print(f"\n🏆 Cheapest model: {cheapest_model} (€{cheapest_cost:.6f})")
```

## See Also
- [`Aggregator`](aggregator.md) - Functionality to aggregate metrics across multiple test runs
- [`Analyzer`](analyzer.md) - Functionality for analyzing and comparing metrics between versions
- [`Models`](models.md) - Data models for metrics and comparison structures
- [`Calculator`](calculator.md) - Utility for single-call metric calculations
- [`Tracker`](tracker.md) - Functionality for tracking and statistical analysis of metrics
