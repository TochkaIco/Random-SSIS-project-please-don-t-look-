import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm

console = Console()
QUIZ_FILE = "quiz.json"

def load_quizzes(): # loads json data into a dictionary
    if not os.path.exists(QUIZ_FILE):
        return []
    try:
        with open(QUIZ_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_quizzes(quizzes):
    with open(QUIZ_FILE, "w") as f:
        json.dump(quizzes, f, indent=4)

def add_questions_to_quiz(quiz_data):
    while True:
        question_text = Prompt.ask("\nEnter question ([bold red]'q'[/bold red] to finish)")
        if question_text.lower() == 'q':
            break
        
        if not question_text.strip():
            console.print("[yellow]Question cannot be empty![/yellow]")
            continue

        answers_input = Prompt.ask("Enter correct answers (separate with ':')")
        if not answers_input.strip():
            console.print("[yellow]Answers cannot be empty![/yellow]")
            continue

        answers = [a.strip().lower() for a in answers_input.split(":") if a.strip()]
        
        quiz_data["questions"].append({
            "question": question_text,
            "answers": answers
        })
        console.print(f"[green]Added question:[/green] {question_text}")

def create_quiz():
    console.clear()
    console.print(Panel("[bold cyan]Create a New Quiz[/bold cyan]", border_style="cyan"))
    
    name = Prompt.ask("Enter quiz name").strip()
    if not name:
        return

    quizzes = load_quizzes()

    quiz_data = next((q for q in quizzes if q["name"].lower() == name.lower()), None)
    if quiz_data:
        console.print(f"[yellow]A quiz named '{name}' already exists. Adding questions to it.[/yellow]")
    else:
        quiz_data = {"name": name, "questions": []}
        quizzes.append(quiz_data)

    add_questions_to_quiz(quiz_data)
    save_quizzes(quizzes)
    console.print("[bold green]Quiz saved successfully![/bold green]")
    Prompt.ask("\nPress Enter to return to menu")

def manage_quizzes(): # Edit / Rename / Delete
    while True:
        quizzes = load_quizzes()
        console.clear()
        console.print(Panel("[bold magenta]Manage Quizzes[/bold magenta]", border_style="magenta"))
        
        if not quizzes:
            console.print("[yellow]No quizzes available.[/yellow]")
            if Confirm.ask("Create one now?"):
                create_quiz()
                continue
            break

        table = Table(title="Existing Quizzes")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Quiz Name", style="white")
        table.add_column("Questions", justify="right", style="green")

        quiz_id = 1
        for q in quizzes:
            table.add_row(str(quiz_id), q["name"], str(len(q["questions"])))

        console.print(table)
        console.print("\n[bold]ID[/bold]: Edit | [bold]d <ID>[/bold]: Delete | [bold]b[/bold]: Back")
        cmd = Prompt.ask("Choice").strip().lower()

        if cmd == 'b':
            break
        elif cmd.startswith('d '):
            try:
                idx = int(cmd.split(' ')[1]) - 1
                if 0 <= idx < len(quizzes):
                    if Confirm.ask(f"Delete '[red]{quizzes[idx]['name']}[/red]'?"):
                        quizzes.pop(idx)
                        save_quizzes(quizzes)
                else:
                    console.print("[red]Invalid ID[/red]")
            except (ValueError, IndexError):
                console.print("[red]Invalid command format[/red]")
            Prompt.ask("Press Enter")
        else:
            try:
                user_choice = int(cmd) - 1
                if 0 <= user_choice < len(quizzes):
                    edit_specific_quiz(user_choice, quizzes)
                else:
                    console.print("[red]Invalid ID[/red]")
                    Prompt.ask("Press Enter")
            except ValueError:
                console.print("[red]Invalid command[/red]")

def edit_specific_quiz(quiz_id, quizzes):
    while True:
        quiz = quizzes[quiz_id]
        console.clear()
        console.print(Panel(f"[bold cyan]Editing: {quiz['name']}[/bold cyan]", border_style="cyan"))
        
        console.print("1. [bold white]Rename Quiz[/bold white]")
        console.print("2. [bold green]Add Questions[/bold green]")
        console.print("3. [bold red]Remove Questions[/bold red]")
        console.print("4. [bold yellow]Back[/bold yellow]")
        
        user_choice = Prompt.ask("Select", choices=["1", "2", "3", "4"])
        
        if user_choice == "1":
            quiz["name"] = Prompt.ask("New name", default=quiz["name"])
            save_quizzes(quizzes)
        elif user_choice == "2":
            add_questions_to_quiz(quiz)
            save_quizzes(quizzes)
        elif user_choice == "3":
            remove_questions_from_quiz(quiz, quizzes)
        else:
            break

def remove_questions_from_quiz(quiz, quizzes):
    while True:
        console.clear()
        console.print(f"[bold red]Remove Questions from: {quiz['name']}[/bold red]\n")
        
        if not quiz["questions"]:
            console.print("[yellow]No questions left![/yellow]")
            Prompt.ask("Press Enter")
            break

        table = Table()
        table.add_column("ID", justify="right")
        table.add_column("Question")

        user_choice = 1
        for q in quiz["questions"]:
            table.add_row(str(user_choice), q["question"])
        
        console.print(table)
        user_choice = Prompt.ask("ID to delete ('b' to back)")
        if user_choice.lower() == 'b': break
        
        try:
            choice_id = int(user_choice) - 1
            if 0 <= choice_id < len(quiz["questions"]):
                quiz["questions"].pop(choice_id)
                save_quizzes(quizzes)
            else:
                console.print("[red]Invalid ID[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")
        Prompt.ask("Press Enter")

def play_quiz(): # Play already created quizzes
    quizzes = load_quizzes()
    if not quizzes: # Gets hit if the quizzes dictionary is empty
        console.print("[bold red]No quizzes available![/bold red]")
        Prompt.ask("Press Enter")
        return

    console.clear()
    table = Table(title="Select a Quiz")
    quiz_id = 1
    for question in quizzes: # Shows a table of all available quizzes
        table.add_row(str(quiz_id), question["name"])
        quiz_id += 1
    console.print(table)
    
    choice_raw = Prompt.ask("Choice ('b' to back)")
    if choice_raw.lower() == 'b': return
        
    try:
        selected = quizzes[int(choice_raw) - 1]
        if not selected["questions"]:
            console.print("[red]No questions here![/red]")
            Prompt.ask("Press Enter")
            return

        score = 0
        console.clear()
        console.print(Panel(f"[bold yellow]Playing: {selected['name']}[/bold yellow]"))

        quiz_id = 1
        for q in selected["questions"]:
            console.print(f"\n[bold]Question {quiz_id}:[/bold] {q['question']}")
            answer = Prompt.ask("Answer").strip().lower()
            if answer in [a.lower() for a in q["answers"]]:
                console.print("[green]Correct![/green]")
                score += 1
            else:
                console.print(f"[red]Wrong![/red] Answer(s): {', '.join(q['answers'])}")

        console.print(Panel(f"Final Score: [bold]{score}/{len(selected['questions'])}[/bold]"))
        Prompt.ask("Press Enter")
    except ValueError:
        console.print("[red]Invalid selection[/red]")
        Prompt.ask("Press Enter")

while True:
    console.clear()
    console.print(Panel.fit("[bold magenta] Welcome to a TUI-based Quiz Game! [/bold magenta]", border_style="bright_magenta"))
    console.print("1. [bold green]Play[/bold green]\n2. [bold cyan]Manage[/bold cyan]\n3. [bold red]Exit[/bold red]")

    user_choice = Prompt.ask("\nSelect", choices=["1", "2", "3"], default=1)
    try:
        user_choice = int(user_choice)
        if user_choice == 1:
            play_quiz()
        elif user_choice == 2:
            manage_quizzes()
        else:
            break
    except ValueError:
        console.print("[red]Invalid input[/red]")