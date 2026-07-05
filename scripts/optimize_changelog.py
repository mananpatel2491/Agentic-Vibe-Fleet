import os
import sys
import argparse
import re
from pathlib import Path
try:
    from google import genai
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: Required packages not found. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Legacy Windows consoles (cp1252) cannot encode characters like '→' that appear in the
# changelog content; replace unencodable characters instead of crashing the preview.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")

def select_model(client, model_override=None):
    """Dynamic model selection as per Pattern Registry (Non-Hardcoded LLM Selection).
    The live `client.models.list()` query is the ONLY source of model IDs — there is
    no static fallback, so a listing failure is a hard error."""
    if model_override:
        return model_override
    try:
        print("Fetching available models...")
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

    # For automation, we pick the first one unless interactive
    return available_models[0].name

def get_logged_files_from_table(table_text):
    """Extracts a set of normalized filenames from a markdown table string."""
    files = set()
    for line in table_text.splitlines():
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                # Column index 3 is 'Files Affected'
                files_raw = parts[3].strip()
                for file_entry in files_raw.split(","):
                    clean_name = file_entry.strip().replace("`", "")
                    # Standardize logic to skip headers and separators
                    if clean_name and not any(x in clean_name for x in ["Files Affected", "---", "Action", "Date"]):
                        # Normalize path for comparison
                        try:
                            # Ensure we normalize to posix and strip any trailing/leading slashes
                            normalized = str(Path(clean_name.strip('/')).as_posix())
                            files.add(normalized)
                        except Exception:
                            continue
    return files

def optimize_changelog(requested_model=None, dry_run=False):
    # 1. Setup Environment
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(f"Error: GOOGLE_API_KEY not found at {env_path}")
        sys.exit(1)

    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    model_id = select_model(client, requested_model)

    structure_file = root / "Project_Structure.md"
    if not structure_file.exists():
        print(f"Error: {structure_file} not found.")
        sys.exit(1)

    # 2. Extract Changelog
    with open(structure_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content to isolate the Changelog table (usually the last section)
    parts = re.split(r"(## Changelog)", content)
    if len(parts) < 3:
        print("Error: Could not find ## Changelog section in Project_Structure.md")
        sys.exit(1)

    preamble = parts[0] + parts[1]
    changelog_table = parts[2].strip()

    original_files = get_logged_files_from_table(changelog_table)

    # 3. Request Optimization
    prompt = f"""
    You are a technical documentation expert. Below is a Markdown table representing a project changelog.
    Your task is to optimize this table for readability:
    1. Consolidate entries that occur on the same date.
    2. CRITICAL: The 'Files Affected' column MUST contain the union of ALL individual filenames from the consolidated rows. Do not use generic descriptions like 'various files'.
    3. Ensure the summary is concise but captures the intent of all merged changes.
    4. Maintain the exact Markdown table structure: | Date | Action | Files Affected | Summary |
    5. Return ONLY the optimized table code, including the header and separators. No conversational text.

    CURRENT TABLE:
    {changelog_table}
    """

    print(f"Optimizing changelog using {model_id}...")
    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        optimized_table = response.text.strip()

        # Sanitize LLM output (remove triple backticks if present)
        optimized_table = re.sub(r"^```markdown\n|```$", "", optimized_table, flags=re.MULTILINE).strip()

        # Validation Check: Ensure no files were lost in optimization
        new_files = get_logged_files_from_table(optimized_table)
        missing_files = original_files - new_files

        if missing_files:
            print(f"\033[91mERROR: Optimization failed integrity check.\033[0m")
            print(f"The following files would be removed from the log, which would break verify_structure.py:")
            for f in missing_files: print(f" - {f}")
            sys.exit(1)

        final_output = f"{preamble}\n\n{optimized_table}\n"

        # 4. Handle Output
        if dry_run:
            print("\n--- DRY RUN: OPTIMIZED TABLE PREVIEW ---")
            print(optimized_table)
            print("\n--- END PREVIEW ---")
        else:
            with open(structure_file, "w", encoding="utf-8") as f:
                f.write(final_output)
            print(f"Successfully updated and optimized {structure_file}")

    except Exception as e:
        print(f"ERROR: The API call failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize the Project_Structure.md changelog using Gemini.")
    parser.add_argument("--model", type=str, help="Specify the Gemini model ID to use.")
    parser.add_argument("--dry-run", action="store_true", help="Preview the changes without writing to file.")
    
    args = parser.parse_args()
    optimize_changelog(requested_model=args.model, dry_run=args.dry_run)
