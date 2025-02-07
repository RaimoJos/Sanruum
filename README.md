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
├── STATS.md
├── data/
│   ├── ai_memory.json
│   ├── faq.json
│   ├── intents.json
│   ├── responses.json
│   ├── session_history.json
│   ├── session_history.json.bak
│   └── user_memory/
├── logs/
├── pyproject.toml
├── qodana.yaml
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
│   ├── ai_system.py
│   ├── constants.py
│   ├── faq_handler.py
│   ├── main.py
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── data/
│   │   │   ├── processed_data/
│   │   │   │   └── processed_text_data.csv
│   │   │   └── raw_data/
│   │   │       └── raw_text_data.csv
│   │   ├── data_loader.py
│   │   ├── dataset_creator.py
│   │   ├── models/
│   │   │   ├── logistic_regression_model.pkl
│   │   │   ├── random_forest_model.pkl
│   │   │   └── svm_model.pkl
│   │   ├── output.png
│   │   ├── train_model.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── preprocessing.py
│   └── utils/
│       ├── __init__.py
│       ├── audio_utils.py
│       ├── logger.py
│       └── web_search.py
├── scripts/
│   ├── add_filename.py
│   ├── generate_tree.py
│   └── update_readme_project_info.py
└── typings/
    └── langdetect.pyi
```
<!-- END_TREE -->
