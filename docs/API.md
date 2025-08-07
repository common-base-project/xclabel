# API Documentation

## LLM Endpoints
| Method | Path | Description | Parameters |
|--------|------|-------------|------------|
| POST | `/api/llm/chat` | Text chat completion | `provider_id`, `model`, `messages` |
| POST | `/api/llm/image` | Generate image | `provider_id`, `model`, `prompt`, `size` |
| POST | `/api/llm/video` | Generate video | `provider_id`, `model`, `prompt`, `duration` |
| POST | `/api/llm/analyze` | Analyze uploaded media | `provider_id`, `model`, `task`, `file` |

All endpoints return JSON with `code` and `data`/`msg` fields. A `code` of `1000` indicates success.

## Provider Management
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/llm/providers` | List configured providers |
| POST | `/api/llm/providers/create` | Create provider |
| PUT/PATCH | `/api/llm/providers/<id>/update` | Update provider |
| DELETE | `/api/llm/providers/<id>/delete` | Delete provider |

Provider fields: `name`, `type`, `base_url`, `api_key`, `is_active`, `extra`.

