# User Guide

1. Configure providers via the `/api/llm/providers` endpoints.
2. Use `/api/llm/chat` to send chat messages to a selected provider and model.
3. `/api/llm/image` and `/api/llm/video` accept prompts to generate media.
4. `/api/llm/analyze` accepts a file upload and returns analysis results.

All requests require a `provider_id` referencing a configured provider.
