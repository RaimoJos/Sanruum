# Sanruum

## Project Structure

<!-- START_TREE -->

```
sanruum/
├── .git/
├── .gitignore
├── .idea/
├── .mypy_cache/
├── .treeignore
├── README.md
├── data/
│   ├── faq.json
│   ├── responses.json
│   ├── session_history.json
│   └── user_memory/
├── logs/
├── pyproject.toml
├── requirements.txt
├── sanruum/
│   ├── __init__.py
│   ├── ai_core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── memory.py
│   │   ├── persistent_memory.py
│   │   ├── processor.py
│   │   ├── response.py
│   │   └── speech/
│   │       ├── __init__.py
│   │       ├── diarization.py
│   │       ├── language_detection.py
│   │       ├── speech_config.py
│   │       ├── speech_recognition.py
│   │       └── text_to_speech.py
│   ├── constants.py
│   ├── faq_handler.py
│   ├── main.py
│   └── utils/
│       ├── __init__.py
│       ├── audio_utils.py
│       └── logger.py
├── scripts/
│   └── generate_tree.py
└── typings/
    └── langdetect.pyi
```

<!-- END_TREE -->
