PUBSPEC AI EXTRACTOR

PubSpec AI Extractor is an experimental AI engineering project that uses a local Large Language Model (LLM) to extract structured metadata from pubspec.yaml files without relying on a traditional YAML parser.

This project intentionally explores how far large language models can act as primary parsers for real-world configuration files.

This is an AI-first experiment. Accuracy is not guaranteed by design.

MOTIVATION

In real software ecosystems, configuration files such as pubspec.yaml:

* Contain comments, nested blocks, and optional fields
* Evolve over time
* Are sometimes partially invalid or inconsistent

Traditional parsers are strict but fragile.
This project investigates whether LLMs can infer structure and intent instead of depending on rigid syntax.

Key questions explored:

* Can an LLM parse pubspec.yaml directly from raw text?
* How does it behave with large, real-world dependency lists?
* What failure modes appear (truncation, invalid JSON)?
* Is partial extraction still valuable?

CORE PRINCIPLES

* Fully AI-driven extraction
* No YAML parser in the main pipeline
* Local LLM only (no cloud APIs)
* End-to-end product-style architecture
* Partial results are preferred over total failure

ARCHITECTURE OVERVIEW

pubspec.yaml
|
v
FastAPI (/extract)
|
v
Local LLM (GGUF via llama.cpp)
|
v
Best-effort JSON output
|
v
CLI or API response

FEATURES

* Local LLM inference (CPU-only supported)
* Dockerized LLM server using llama.cpp
* REST API built with FastAPI
* CLI tool that accepts file paths
* Handles large real-world pubspec.yaml files
* Returns partial data instead of crashing
* No YAML parsing library used for extraction


EXAMPLE

Input pubspec.yaml:

dependencies:
flutter:
sdk: flutter
http: ^0.13.4
firebase_core: ^1.20.0

Example AI output:

{
"name": "module_complete",
"version": "1.0.0+1",
"environment": {
"sdk": ">=2.17.1 <3.0.0"
},
"dependencies": [
{
"name": "flutter",
"type": "sdk",
"details": { "sdk": "flutter" }
},
{
"name": "http",
"type": "hosted",
"constraint": "^0.13.4"
}
]
}

The output may be partial or truncated. This behavior is expected.

RUNNING THE PROJECT

1. Build and start services

docker-compose up -d --build

2. Health check

curl [http://localhost:8000/health](http://localhost:8000/health)

3. Run CLI extraction

python cli/pubspec_ai.py --input ./test_files/pubspec.yml

LOCAL LLM SETUP

* Uses GGUF models such as Phi-3 or LLaMA
* Served via llama.cpp
* CPU-only inference supported
* Model files are not committed to GitHub

KNOWN LIMITATIONS

* High latency when running on CPU
* LLM may output invalid or truncated JSON
* Large dependency blocks may be cut off
* Output quality depends heavily on prompt design

These limitations are intentional research trade-offs.

WHAT THIS PROJECT DEMONSTRATES

* Real-world AI system integration
* Prompt engineering under strict constraints
* Dockerized local LLM deployment
* Handling LLM failure modes gracefully
* Trade-offs between AI parsing and deterministic parsers

POSSIBLE FUTURE WORK

* Streaming JSON generation
* Schema-aware decoding
* Automatic retry and repair loops
* Hybrid AI plus YAML parser comparison
* Benchmarking against classical parsers
