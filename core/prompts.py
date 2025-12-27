EXTRACT_PROMPT = """You are a strict information-extraction engine.

Extract metadata from the provided pubspec.yaml text into EXACTLY this JSON structure.

Schema:
{
  "name": string|null,
  "version": string|null,
  "environment": {
    "sdk": string|null
  },
  "dependencies": [
    {
      "name": string,
      "type": "hosted" | "sdk" | "git" | "path" | "unknown",
      "constraint": string|null,
      "details": object|null
    }
  ],
  "dev_dependencies": [
    {
      "name": string,
      "type": "hosted" | "sdk" | "git" | "path" | "unknown",
      "constraint": string|null,
      "details": object|null
    }
  ]
}

Rules:
- Output ONLY valid JSON
- Do NOT use markdown or ``` fences
- Ignore comments
- One array element per dependency
- "type" meanings:
  - "hosted": version constraint like "^1.2.3"
  - "sdk": Flutter/Dart SDK dependency
  - "git": git dependency
  - "path": local path dependency
- "constraint" is the version string if present, otherwise null
- "details" may include nested fields (e.g. {"sdk":"flutter"}) or null
- Use null for unknown values
- Arrays must exist even if empty

pubspec.yaml:
{PUBSPEC_TEXT}
""".strip()
