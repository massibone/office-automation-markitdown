from pathlib import Path
from markitdown import MarkItDown

INPUT_DIR = Path("/office-automation-markitdown/input")
OUTPUT_DIR = Path("/office-automation-markitdown/output")
SUPPORTED_EXTENSIONS = {".docx", ".xlsx", ".pdf", ".pptx", ".txt", ".csv", ".html", ".xml"}


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    md = MarkItDown()

    files = [
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print("Nessun file supportato trovato in input/.")
        return

    for file_path in files:
        try:
            result = md.convert(str(file_path))
            output_file = OUTPUT_DIR / f"{file_path.stem}.md"
            output_file.write_text(result.text_content, encoding="utf-8")
            print(f"Convertito: {file_path.name} -> {output_file.name}")
        except Exception as exc:
            print(f"Errore su {file_path.name}: {exc}")


if __name__ == "__main__":
    main()
