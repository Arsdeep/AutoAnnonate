# README

## Overview

This Python script processes all the files in a source directory, adds comments to the code using Google's Generative AI model (Gemini), and saves the processed files to a specified destination directory. It also supports excluding certain file types and directories, including hidden directories.

## Prerequisites

1. **Python 3.7 or higher**: Ensure you have Python installed on your system.
2. **Google Generative AI SDK**: Install the `google-generativeai` package.
3. **GEMINI API Key**: You need a GEMINI API key to use the Generative AI model.

## Setup

1. **Install Required Packages**:
    ```bash
    pip install google-generativeai
    ```

2. **Set GEMINI API Key**:
    Replace `'your api'` with your actual GEMINI API key in the script.

3. **Exclusion Lists**:
    - `extension_exclusion_list.txt`: Contains file extensions to exclude.
    - `folder_exclusion_list.txt`: Contains folder names to exclude.
    If these files do not exist, the script will prompt you to create default lists.

## Usage

The script can be run from the command line with various options:

```bash
python script.py [--src SRC_DIRECTORY] [--out DST_DIRECTORY] [--excludeHiddenDirs true|false]
```

### Options

- `--src`: Sets the source directory. Default is the current directory (`./`).
- `--out`: Sets the destination directory. Default is `./Generated`.
- `--excludeHiddenDirs`: Exclude hidden directories. Default is `true`.

### Example

To process files from a source directory (`./source`) and save them to a destination directory (`./output`) while excluding hidden directories:

```bash
python script.py --src ./source --out ./output --excludeHiddenDirs true
```

## Exclusion Lists

The script supports exclusion lists for file extensions and folder names:

- **File Extensions**:
    - Default list includes common binary and non-code file extensions such as `.ico`, `.jpg`, `.pdf`, etc.
- **Folders**:
    - Default list includes common temporary and environment directories such as `__pycache__`, `node_modules`, `.git`, etc.

These lists are stored in `extension_exclusion_list.txt` and `folder_exclusion_list.txt`, respectively. If these files do not exist, the script will prompt to create them with default values.

## Note

- Ensure that the destination directory is different from the source directory to avoid infinite loops and potential data loss.
- The script assumes that the content in files is UTF-8 encoded.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For issues, please open a ticket on the project's GitHub repository.