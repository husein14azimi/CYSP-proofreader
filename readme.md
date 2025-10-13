# CYSP Proofreader

AI-powered dictation correction tool for conference editors working with scientific articles.

## Features

- **AI-Powered Correction**: Uses advanced AI models to fix spelling and dictation errors
- **Single Output**: Generates one clean document with AI corrections
- **Multiple AI Models**: Support for DeepSeek, Claude, GPT, and other models via OpenRouter
- **Farsi/English Support**: Handles mixed Persian and English content
- **Privacy Focused**: Documents are processed securely through OpenRouter API
- **User-Friendly Interface**: Simple tabbed interface for easy operation

## Requirements

- Windows 10 or 11
- OpenRouter API key (free tier available)
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
2. **Configure Privacy Settings**: After getting your API key, visit [OpenRouter Privacy Settings](https://openrouter.ai/settings/privacy) and enable:
   - "Enable free endpoints that may train on inputs"
   - "Enable free endpoints that may publish prompts"
3. **Select Document**: Choose a DOCX file to process
4. **Configure API**: Enter your OpenRouter API key and select an AI model
5. **Process**: Click "Process Document" to start AI correction
6. **Review**: Check the generated output file in the same directory

## Output File

- `Document_Edited.docx`: Clean version with AI corrections

## Supported AI Models

- DeepSeek v3.1 Free (`deepseek/deepseek-chat-v3.1:free`)
- Microsoft Phi-3 Mini Free
- Google Gemma 7B IT Free
- Mistral 7B Free
- And many others via OpenRouter

## Development

### Project Structure
```
cysp-proofreader/
├── main.py # Entry point
├── config/ # Configuration files
├── core/ # Core processing modules
├── ui/ # User interface components
├── utils/ # Utility functions
└── requirements.txt # Dependencies
```


### Building from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run development version
python main.py

# Build executable
python build.py
```

License
MIT License - see LICENSE file for details

Support
For issues and feature requests, please open an issue on GitHub.

> **Note**
>
> The free api key might run out of credit/quota if the docx file is heavy/big. for such files, splitting is recommended. you can also check the number of tokens in the program logs.