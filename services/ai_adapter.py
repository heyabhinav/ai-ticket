# app/services/ai_adapter.py

import json
from typing import Tuple
from openai import AzureOpenAI
from app.config import settings

# Create a single reusable client
client = AzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
)

def classify_text(text: str) -> Tuple[str, str, str, float]:
    """
    Use Azure OpenAI (gpt-5-nano) to classify a ticket.

    Returns:
        category:   e.g. "Network", "Database", "Access", ...
        priority:   "High" | "Medium" | "Low"
        suggestion: short fix recommendation
        confidence: float between 0.0 and 1.0 (model's self-reported confidence)
    """

    system_prompt = """
You are an IT ticket triage assistant.

You MUST classify each ticket into exactly one of these categories:
- Network
- Database
- Application
- Access
- Hardware
- Other

You must:
1) Choose a category.
2) Assign a priority: High, Medium, or Low.
3) Suggest a short, practical fix (1–3 sentences).
4) Give a confidence score (0.0 to 1.0) representing how likely the suggested fix will resolve the issue.

Rules:
- High: production outage, many users impacted, security or critical data issues.
- Medium: single service affected, degraded performance, workaround exists.
- Low: minor bugs, cosmetic problems, general queries.

Return ONLY valid JSON, no explanation, in this exact format:
{
  "category": "<one category>",
  "priority": "<High|Medium|Low>",
  "suggestion": "<short suggested fix>",
  "confidence": <number between 0.0 and 1.0>
}
""".strip()

    response = client.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,  # deployment name for gpt-5-nano
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )

    content = response.choices[0].message.content
    data = json.loads(content)

    category = data.get("category", "Other")
    priority = data.get("priority", "Low")
    suggestion = data.get("suggestion", "No suggestion provided.")
    raw_conf = data.get("confidence", 0.7)

    try:
        confidence = float(raw_conf)
    except (TypeError, ValueError):
        confidence = 0.7

    # clamp value into [0.0, 1.0]
    confidence = max(0.0, min(1.0, confidence))

    return category, priority, suggestion, confidence
