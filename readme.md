# CYSP Proofreader Project

AI-powered dictation correction tool for conference editors working with scientific articles.

## Features

- **AI-Powered Correction**: Uses advanced AI models to fix spelling and dictation errors
- **Dual Output**: Generates both clean and highlighted versions of edited documents
- **Multiple AI Models**: Support for models via OpenRouter
- **Farsi/English Support**: Handles mixed Persian and English content
- **Privacy Focused**: Documents are processed securely through OpenRouter API
- **User-Friendly Interface**: Simple tabbed interface for easy operation

## Requirements

- Windows 10 or 11
- OpenRouter API key (free tier acceptable)
- Microsoft Word for viewing output documents

## Installation

### Option 1: Pre-built Executable (Recommended)
Download the latest release from the releases page.

### Option 2: From Source
1. Install Python 3.8 or higher
2. Clone this repository
3. Run `pip install -r requirements.txt`
4. Run `python main.py`


## Usage

1. **Get API Key**: Sign up at [OpenRouter](https://openrouter.ai/) and get your free API key
2. **Select Document**: (having the program running,) Choose a DOCX file to process
3. **Configure API**: Enter your OpenRouter API key and select an AI model. If you're entering a custom model, enter the token limit either.
4. **Process**: Click "Process Document" to start AI correction
5. **Review**: Check the generated output files in the same directory

## Output Files

Only the reviewed DOCX file.

## Default AI Models

- DeepSeek v3 (default, 128K token limit)
- Claude 3 Haiku (200K token limit)
- GPT-3.5 Turbo (16K token limit)
- Mistral Tiny (32K token limit)


## Contributing to develop and improve this project

If you want to participate in developing this project, after getting the code from the repository, you can run the project via

```bash
python main.py
```

and you can build the EXE file via

```bash
python build.py
```
the output file will be in the `dist` or `dist_package` directory. 


## Usage in CYSP
after the reviewed/revised docx file is served, you can see the modified segments using Microsoft Word (or other programs like LibreOffice Writer)'s compare tool.

## Next steps in improvement if you are interested:
- UI
- PYPI distribution (the `setup.py`)

<br>
<br>
<br>

This project was developed on vibe coding mode by the help of QWEN Coder, a powerful coding AI.

Thank you and good luck!