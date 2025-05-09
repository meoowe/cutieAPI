import requests
import json
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

def get_user_input():
    """Gets all necessary input from the user."""
    method_choices = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    method = Prompt.ask(
        "Enter HTTP method",
        choices=method_choices,
        default="GET"
    ).upper()

    url = Prompt.ask("Enter the full API URL (e.g., http://localhost:8000/items)")
    while not (url.startswith("http://") or url.startswith("https://")):
        console.print("[bold red]Invalid URL. Must start with 'http://' or 'https://'.[/bold red]")
        url = Prompt.ask("Enter the full API URL")

    headers = {}
    if Confirm.ask("Add custom headers?", default=False):
        console.print("Enter headers one by one (e.g., Authorization: Bearer token). Press Enter on an empty line to finish.")
        while True:
            header_input = Prompt.ask("Header (or leave empty to finish)").strip()
            if not header_input:
                break
            if ":" not in header_input:
                console.print("[yellow]Warning: Header should be in 'Key: Value' format. Skipping.[/yellow]")
                continue
            key, value = header_input.split(":", 1)
            headers[key.strip()] = value.strip()

    data_payload = None
    json_payload = None

    if method in ["POST", "PUT", "PATCH"]:
        body_type = Prompt.ask(
            "Request body type?",
            choices=["json", "form", "raw", "none"],
            default="json"
        ).lower()

        if body_type == "json":
            console.print("Enter JSON body (you can paste multi-line JSON). [i]Press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to finish input.[/i]")
            json_lines = []
            try:
                while True:
                    line = input() # Using built-in input for multi-line
                    json_lines.append(line)
            except EOFError:
                pass
            json_string = "\n".join(json_lines)
            try:
                json_payload = json.loads(json_string)
                if 'Content-Type' not in (h.lower() for h in headers.keys()): # Check case-insensitively
                     headers['Content-Type'] = 'application/json'
            except json.JSONDecodeError as e:
                console.print(f"[bold red]Invalid JSON input: {e}[/bold red]")
                return None # Indicate failure
            except Exception: # Catch other potential issues during input
                console.print(f"[bold red]Error reading JSON input.[/bold red]")
                return None


        elif body_type == "form":
            console.print("Enter form data (key=value, one per line). Press Enter on an empty line to finish.")
            form_data_dict = {}
            while True:
                entry = Prompt.ask("Form data (key=value, or empty to finish)").strip()
                if not entry:
                    break
                if "=" not in entry:
                    console.print("[yellow]Warning: Form data should be 'key=value'. Skipping.[/yellow]")
                    continue
                key, value = entry.split("=", 1)
                form_data_dict[key.strip()] = value.strip()
            data_payload = form_data_dict
            if 'Content-Type' not in (h.lower() for h in headers.keys()):
                headers['Content-Type'] = 'application/x-www-form-urlencoded'

        elif body_type == "raw":
            console.print("Enter raw text body. [i]Press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to finish input.[/i]")
            raw_lines = []
            try:
                while True:
                    line = input()
                    raw_lines.append(line)
            except EOFError:
                pass
            data_payload = "\n".join(raw_lines)
            # User should set Content-Type manually for raw if needed

    return method, url, headers, data_payload, json_payload


def make_api_request(method, url, headers, data_payload, json_payload):
    """Makes the API request and prints the response."""
    console.rule(f"[bold blue]Sending {method} request to {url}")

    if headers:
        console.print("\n[bold]Headers Sent:[/bold]")
        for key, value in headers.items():
            console.print(f"  {key}: {value}")

    if json_payload:
        console.print("\n[bold]JSON Body Sent:[/bold]")
        json_str_sent = json.dumps(json_payload, indent=2)
        syntax = Syntax(json_str_sent, "json", theme="monokai", line_numbers=True)
        console.print(syntax)
    elif data_payload and isinstance(data_payload, dict): # Form data
        console.print("\n[bold]Form Data Sent:[/bold]")
        for key, value in data_payload.items():
            console.print(f"  {key}: {value}")
    elif data_payload and isinstance(data_payload, str): # Raw data
        console.print("\n[bold]Raw Body Sent:[/bold]")
        console.print(Panel(data_payload, expand=False))


    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            data=data_payload, # For form data or raw text
            json=json_payload, # For JSON data (requests handles serialization)
            timeout=30 # 30 seconds timeout
        )
        console.rule("[bold green]Response Received")
        console.print(f"[bold]Status Code:[/bold] {response.status_code} {response.reason}")

        console.print("\n[bold]Response Headers:[/bold]")
        header_table = Table(show_header=False, box=None)
        for key, value in response.headers.items():
            header_table.add_row(f"[cyan]{key}[/cyan]", value)
        console.print(header_table)

        console.print("\n[bold]Response Body:[/bold]")
        content_type = response.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            try:
                json_body = response.json()
                json_str_received = json.dumps(json_body, indent=2)
                syntax = Syntax(json_str_received, "json", theme="monokai", line_numbers=True)
                console.print(syntax)
            except json.JSONDecodeError:
                console.print(Panel(response.text, title="Raw Text (Not valid JSON)", expand=False, border_style="yellow"))
        elif "text/html" in content_type:
            syntax = Syntax(response.text, "html", theme="monokai", line_numbers=True)
            console.print(syntax)
        elif "text/" in content_type:
            console.print(Panel(response.text, title="Plain Text", expand=False))
        else:
            console.print(f"Non-text content type: {content_type}. Displaying as raw bytes if possible, or basic text.")
            # For binary data, you might want to save to a file or show limited output.
            # For simplicity, we'll just try to print its text representation if available.
            try:
                console.print(Panel(response.text, title=f"Raw Content ({content_type})", expand=False))
            except Exception as e:
                 console.print(f"[red]Could not display binary content: {e}[/red]")


    except requests.exceptions.Timeout:
        console.print("[bold red]Error: Request timed out.[/bold red]")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Could not connect to the server. Is the URL correct and the server running?[/bold red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
    console.rule()


if __name__ == "__main__":
    console.print(Panel("🚀 API Buddy v1.0 🚀", title_align="center", expand=False))
    while True:
        inputs = get_user_input()
        if inputs: # If user didn't abort due to bad JSON
            method, url, headers, data_payload, json_payload = inputs
            make_api_request(method, url, headers, data_payload, json_payload)

        if not Confirm.ask("\nMake another request?", default=True):
            break
    console.print("👋 Goodbye!")
