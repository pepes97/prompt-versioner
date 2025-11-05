# Pricing Commands

Commands for viewing model pricing information and estimating costs.

## Overview

The pricing commands help you understand the cost of using different LLM models and estimate expenses for your specific use cases. All pricing is calculated per million tokens and displayed in EUR.

---

## `models`

List all available LLM models with their pricing information.

### Usage

```bash
pv models [OPTIONS]
```

### Options

- `--format {table,json}` - Output format (default: table)
- `--sort-by {name,input,output,total}` - Sort field (default: name)
- `--filter TEXT` - Filter models by name (case-insensitive)
- `--limit INTEGER` - Limit number of models displayed

### Examples

**List all models**
```bash
pv models
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Model Name            ┃ Input Price        ┃ Output Price       ┃ Avg Cost          ┃
┃                       ┃ (per 1M tokens)    ┃ (per 1M tokens)    ┃ (500in+500out)    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ claude-opus-4-1       │ €13.80             │ €69.00             │ €0.041400         │
│ claude-sonnet-4-5     │ €5.06              │ €23.00             │ €0.014030         │
│ gpt-4o                │ €1.15              │ €4.60              │ €0.002875         │
│ gpt-4o-mini           │ €0.18              │ €0.73              │ €0.000455         │
│ mistral-small-3-1     │ €0.09              │ €0.28              │ €0.000185         │
└───────────────────────┴────────────────────┴────────────────────┴───────────────────┘

ℹ Total models: 16

Example: Cost for 1,000 input + 500 output tokens:
  mistral-small-3-1            €0.000370
  gpt-5-nano                   €0.000510
  gpt-4o-mini                  €0.000545
```

**Sort by input price**
```bash
pv models --sort-by input
```

**Sort by total average cost**
```bash
pv models --sort-by total
```

**Filter GPT models only**
```bash
pv models --filter gpt
```

**Show top 10 cheapest models**
```bash
pv models --sort-by total --limit 10
```

**Export to JSON**
```bash
pv models --format json > models.json
```

JSON output:
```json
[
  {
    "name": "gpt-4o",
    "input_price_per_1m": 1.15,
    "output_price_per_1m": 4.60,
    "currency": "EUR"
  },
  {
    "name": "gpt-4o-mini",
    "input_price_per_1m": 0.18,
    "output_price_per_1m": 0.73,
    "currency": "EUR"
  }
]
```

---

## `estimate-cost`

Estimate the cost for a specific model and token usage pattern.

### Usage

```bash
pv estimate-cost MODEL_NAME INPUT_TOKENS OUTPUT_TOKENS [OPTIONS]
```

### Arguments

- `MODEL_NAME` - Name of the model (e.g., "gpt-4o", "claude-sonnet-4")
- `INPUT_TOKENS` - Number of input tokens per call
- `OUTPUT_TOKENS` - Number of output tokens per call

### Options

- `--calls INTEGER` - Number of API calls to estimate (default: 1)

### Examples

**Estimate single call**
```bash
pv estimate-cost gpt-4o 1000 500
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Metric                 ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Input tokens per call  │ 1,000        │
│ Output tokens per call │ 500          │
│ Number of calls        │ 1            │
│ Total input tokens     │ 1,000        │
│ Total output tokens    │ 500          │
│                        │              │
│ Cost per call          │ €0.003450    │
│ Total cost             │ €0.0035      │
└────────────────────────┴──────────────┘
```

**Estimate 100 calls**
```bash
pv estimate-cost gpt-4o-mini 1000 500 --calls 100
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Metric                 ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Input tokens per call  │ 1,000        │
│ Output tokens per call │ 500          │
│ Number of calls        │ 100          │
│ Total input tokens     │ 100,000      │
│ Total output tokens    │ 50,000       │
│                        │              │
│ Cost per call          │ €0.000545    │
│ Total cost             │ €0.0545      │
└────────────────────────┴──────────────┘
```

**Model not found error**
```bash
pv estimate-cost unknown-model 1000 500
```

Output:
```
⚠ Model 'unknown-model' not found in pricing database

Available models:
  • claude-haiku-4
  • claude-opus-4
  • claude-opus-4-1
  • claude-sonnet-4
  • claude-sonnet-4-5

Use 'pv models' to see all 16 models
```

---

## `compare-costs`

Compare costs across all available models for a given token usage pattern.

### Usage

```bash
pv compare-costs INPUT_TOKENS OUTPUT_TOKENS [OPTIONS]
```

### Arguments

- `INPUT_TOKENS` - Number of input tokens
- `OUTPUT_TOKENS` - Number of output tokens

### Options

- `--top INTEGER` - Show only top N cheapest models (default: 5)

### Examples

**Compare top 5 cheapest models**
```bash
pv compare-costs 1000 500
```

Output:
```
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Rank  ┃ Model Name            ┃ Cost       ┃ Relative ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│     1 │ mistral-small-3-1     │ €0.000370  │ 1.0x     │
│     2 │ gpt-5-nano            │ €0.000510  │ 1.4x     │
│     3 │ gpt-4o-mini           │ €0.000545  │ 1.5x     │
│     4 │ mistral-nemo          │ €0.000700  │ 1.9x     │
│     5 │ gpt-4-1-mini          │ €0.001285  │ 3.5x     │
└───────┴───────────────────────┴────────────┴──────────┘

ℹ Showing top 5 of 16 models
Use --top 16 to see all models
```

**Compare all models**
```bash
pv compare-costs 1000 500 --top 100
```

**Compare top 10**
```bash
pv compare-costs 1000 500 --top 10
```

---

## Supported Models

The pricing database includes the following model families:

### Claude (Anthropic)
- `claude-opus-4-1`, `claude-opus-4`
- `claude-sonnet-4-5`, `claude-sonnet-4`
- `claude-haiku-4`

### GPT (OpenAI)
- `gpt-5`, `gpt-5-mini`, `gpt-5-nano`
- `gpt-4-1`, `gpt-4-1-mini`
- `gpt-4o`, `gpt-4o-mini`

### Mistral
- `mistral-large-24-11`
- `mistral-medium-3`
- `mistral-small-3-1`
- `mistral-nemo`

---

## Use Cases

### 1. Find the cheapest model for your use case
```bash
pv compare-costs 2000 1000 --top 5
```

### 2. Estimate monthly costs
```bash
# 10,000 calls per month with 1000 input + 500 output tokens
pv estimate-cost gpt-4o-mini 1000 500 --calls 10000
```

### 3. Compare specific model families
```bash
# GPT models
pv models --filter gpt --sort-by total

# Claude models
pv models --filter claude --sort-by total

# Mistral models
pv models --filter mistral --sort-by total
```

### 4. Budget planning
```bash
# Export to JSON for analysis
pv models --format json > pricing_data.json

# Compare across different token patterns
pv compare-costs 500 250   # Short interactions
pv compare-costs 2000 1000 # Medium interactions
pv compare-costs 8000 4000 # Long interactions
```

---

## Tips

1. **Cost Optimization**: Use `compare-costs` to find the most cost-effective model for your token patterns
2. **Batch Estimation**: Use `--calls` option to estimate costs for multiple API calls
3. **Filter by Provider**: Use `--filter` to compare models from specific providers
4. **Export Data**: Use `--format json` to export pricing data for further analysis
5. **Sort Strategically**: Sort by `total` to see the most cost-effective models for balanced workloads

---

## Related Commands

- [`show`](commands.md#show) - View metrics for specific prompt versions
- [`compare`](commands.md#compare) - Compare performance across versions
- [`dashboard`](commands.md#dashboard) - View metrics in web interface
