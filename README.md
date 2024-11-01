# Dynamic PII Masking Tool

A real-time PII (Personally Identifiable Information) detection and masking tool powered by Llama 2 LLM. This tool provides dynamic identification and consistent masking of sensitive information in text data.

## Features

### PII Detection
- Pattern-based detection using regex
- LLM-powered sensitive information detection
- Named Entity Recognition (NER)
- Confidence scoring
- Custom pattern support

### Masking
- Consistent hash-based masking
- Configurable mask patterns
- Context preservation
- Reversible masking (with proper authorization)

### Performance
- Caching system
- Batch processing
- GPU acceleration
- Multi-threading support

## 🛠Installation

1. Clone the repository

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

### Basic Usage
```python
from pii_masker import PIIMaskingTool

# Initialize tool
masker = PIIMaskingTool()

# Process text
text = "Contact John at john.doe@email.com"
result = masker.process_text(text)

print(result['masked_text'])
# Output: "Contact [PERSON_123] at [EMAIL_456]"
```

### Custom Configuration
```python
from pii_masker.config import Settings

settings = Settings(
    MIN_CONFIDENCE_SCORE=0.9,
    MASK_PATTERNS={"email": "[EMAIL_REMOVED]"}
)

masker = PIIMaskingTool(settings=settings)
```

### Batch Processing
```python
texts = ["Text 1 with PII", "Text 2 with PII"]
results = masker.process_batch(texts)
```

##  Configuration

Key settings in `.env`:
```env
MODEL_PATH=meta-llama/Llama-2-7b
MIN_CONFIDENCE_SCORE=0.85
CACHE_ENABLED=true
```
