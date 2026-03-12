# TUI Quiz Game

A terminal-based quiz application that allows you to play, create, and manage quizzes with a polished interface using the `rich` library.

## Features

- **Quizzes**: Test your knowledge with existing quizzes. Supports multiple correct answers for a single question.
- **Manage Quizzes**: 
  - Create new quizzes with custom names.
  - Add questions to existing quizzes.
  - Rename or delete entries (specific questions or complete quizzes).
- **Persistent Storage**: All quizzes and questions are saved in `quiz.json`.
- **Beautiful TUI**: Built with `rich` for a formatted terminal look.

You can look into the `rich` library more by taking a look at this repo -> https://github.com/Textualize/rich

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TochkaIco/ssis-programming-1-tui-based-quiz-game.git
   cd ssis-programming-1-tui-based-quiz-game
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the application:

```bash
python main.py
```

## Data Format

Quizzes are stored in `quiz.json` with the following structure:
```json
[
    {
        "name": "Quiz Name",
        "questions": [
            {
                "question": "What is 2+2?",
                "answers": ["4", "four"]
            }
        ]
    }
]
```

## To-do
- [x] Implement general logic
- [x] Add styling with `rich`
- [x] Add quiz templates (Python Essentials)
- [ ] Support for multiple-choice questions (A, B, C, D)
- [ ] Add support for users and scoreboards