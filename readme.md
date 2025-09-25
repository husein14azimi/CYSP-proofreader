# Conference Editing Assistant

AI-powered dictation correction tool for conference editors working with scientific articles.

## Features

- **AI-Powered Correction**: Uses advanced AI models to fix spelling and dictation errors
- **Dual Output**: Generates both clean and highlighted versions of edited documents
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
2. **Select Document**: Choose a DOCX file to process
3. **Configure API**: Enter your OpenRouter API key and select an AI model
4. **Process**: Click "Process Document" to start AI correction
5. **Review**: Check the generated output files in the same directory

## Output Files

- `Document_Edited_Clean.docx`: Clean version with corrections
- `Document_Edited_Highlighted.docx`: Version with visual highlighting of changes

## Supported AI Models

- DeepSeek v3 (default, 128K token limit)
- Claude 3 Haiku (200K token limit)
- GPT-3.5 Turbo (16K token limit)
- Mistral Tiny (32K token limit)

## Development

### Project Structure







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