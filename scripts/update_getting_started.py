import os
import sys
import argparse
from pathlib import Path
try:
    from google import genai
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Required packages not found.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Legacy Windows consoles (cp1252) cannot encode all characters LLM output may contain;
# replace unencodable characters instead of crashing the preview/status output.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

def select_model(client, model_override=None):
    """Resolve the Gemini model to use, in priority order:
    1. an explicit --model override (automation-first bypass),
    2. an interactive pick from the live model list,
    3. index 0 as the default (empty/invalid input, or non-interactive stdin).
    Dynamic `client.models.list()` is the ONLY source of model IDs (Non-Hardcoded
    LLM Selection pattern) — a listing failure is a hard error, never a fallback."""
    if model_override:
        print(f"Using model override: {model_override}")
        return model_override

    print("Fetching available models...")
    try:
        # Filter for models that support generating content
        available_models = [
            m for m in client.models.list()
            if 'generateContent' in m.supported_actions
        ]
    except Exception as e:
        print(f"ERROR: Could not list models ({e}).")
        print("Dynamic model selection is required (Non-Hardcoded LLM Selection pattern); no static fallback exists. Aborting.")
        sys.exit(1)

    if not available_models:
        print("ERROR: The API returned no models supporting generateContent for this key. Aborting.")
        sys.exit(1)

    default = available_models[0].name
    print("\nAvailable Gemini Models:")
    for i, m in enumerate(available_models):
        print(f" [{i}] {m.name} ({m.display_name})")
    try:
        choice = input(f"\nSelect a model index [Enter for default 0: {default}]: ").strip()
    except EOFError:
        # Non-interactive stdin (CI / piped) -> use the default without blocking.
        choice = ""
    if choice.isdigit() and int(choice) < len(available_models):
        return available_models[int(choice)].name
    return default

def update_docs(requested_model=None, dry_run=False):
    # 1. Load environment variables from .env file if it exists
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    load_dotenv(dotenv_path=env_path)

    # 2. Setup API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(f"Error: GOOGLE_API_KEY not found in environment or at {env_path}")
        print("Please ensure your API key is set before running.")
        sys.exit(1)

    # Force 'v1' API version to avoid 404s common in the v1beta endpoint
    # for specific model aliases like 'gemini-1.5-flash'.
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    model_id = select_model(client, requested_model)

    # 3. Define the prompt
    prompt = """
    Explain how to use Gemini Code Assist. 
    Specifically cover: 
    1. What is Agent mode and what happens when I do not use it?
    2. What is the Preview option in the context of code applications and models?
    3. How to use the Fleet's Maintenance Skills.
    4. The 'Prompt Architect' workflow: Using generate_bootstrap_prompt.py to start every new feature or bug fix with high-context planning.
    Format the output as a clean Markdown document suitable for a 'Getting Started' guide.
    """

    print("Querying Gemini API for latest documentation...")
    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        content = response.text

        # 4. Determine file path
        target_file = root / "GEMINI_Getting_Started.md"

        output_content = f"# Getting Started with Gemini Code Assist (Auto-Updated)\n\n{content}\n\n---\n*Last updated via scripts/update_getting_started.py*"

        # 5. Write the file
        if dry_run:
            print("\n--- DRY RUN: OUTPUT PREVIEW ---")
            print(output_content)
            print("--- END PREVIEW ---")
        else:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"Successfully updated {target_file}")

    except Exception as e:
        print(f"ERROR: The API call failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update Gemini onboarding docs via API.")
    parser.add_argument("--model", type=str, help="Specify the Gemini model ID to use (bypasses selection).")
    parser.add_argument("--dry-run", action="store_true", help="Preview the output without writing to the file.")
    
    args = parser.parse_args()
    update_docs(requested_model=args.model, dry_run=args.dry_run)