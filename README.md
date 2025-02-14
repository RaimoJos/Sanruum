# Sanruum

## Project Structure

<!-- START_TREE -->
```
sanruum/
├── .flake8
├── .git/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── dependabot.yml
│   └── workflows/
│       ├── python-app.yml
│       └── stale.yml
├── .gitignore
├── .idea/
├── .mypy_cache/
├── .pre-commit-config.yaml
├── .pytest_cache/
├── .treeignore
├── README.md
├── data/
│   ├── custom_substitutions.csv
│   ├── faq.json
│   ├── ignore_spellcheck_words.txt
│   ├── intents.json
│   ├── responses.json
│   ├── test_text.txt
│   └── user_memory/
├── dist/
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
│   ├── monitor/
│   │   ├── __init__.py
│   │   └── monitor.py
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── data/
│   │   │   ├── processed_data/
│   │   │   └── raw_data/
│   │   ├── data_loader.py
│   │   ├── dataset_creator.py
│   │   ├── models/
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
│   ├── check_project.py
│   ├── generate_tree.py
│   └── update_readme_project_info.py
├── tests/
│   ├── __init__.py
│   ├── ai_core/
│   │   ├── __init__.py
│   │   ├── diarization_test.py
│   │   ├── language_detection_test.py
│   │   ├── memory_test.py
│   │   ├── persistent_memory_test.py
│   │   ├── processor_test.py
│   │   ├── response_test.py
│   │   ├── speech_config_test.py
│   │   ├── speech_recognition_test.py
│   │   └── text_to_speech_test.py
│   ├── monitor/
│   │   ├── __init__.py
│   │   └── monitor_test.py
│   └── utils/
│       ├── __init__.py
│       └── audio_utils_test.py
└── typings/
    └── langdetect.pyi
```
<!-- END_TREE -->
