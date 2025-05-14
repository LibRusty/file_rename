import os
import subprocess
import re
from pathlib import Path

app_dir = Path(__file__).parent
djvused_path = app_dir / 'DjVuLibre' / 'djvused.exe'

def decode_djvu_string(raw_value):
    try:
        if '\\' in raw_value:
            bytes_value = bytes(int(x, 8) for x in re.findall(r'\\(\d{3})', raw_value))
            return bytes_value.decode('utf-8')
        return raw_value
    except Exception:
        return raw_value

def format_djvu_string(value):
    value = re.sub(r'([а-яА-ЯёЁ])([A-Za-z])', r'\1 \2', value)
    value = re.sub(r'([A-Za-z])([а-яА-ЯёЁ])', r'\1 \2', value)

    value = re.sub(r'([a-zа-яё])([A-ZА-ЯЁ])', r'\1 \2', value)

    return value

def extract_djvu_metadata(file_path):
    if not djvused_path.exists():
        raise FileNotFoundError(f"Не найден djvused: {djvused_path}")

    try:
        result = subprocess.run(
            [str(djvused_path), '-e', 'print-meta', file_path],
            capture_output=True, text=True, check=True, encoding='latin1'
        )
        raw_output = result.stdout.strip()
        
        if not raw_output:
            print("Метаданные не найдены или вывод пуст.")
        
        metadata = {}
        for line in raw_output.splitlines():
            try:
                if '"' not in line:
                    continue
                
                key_part, value_part = line.split('"', 1)
                key = key_part.split('=')[0].strip()
                value = value_part.rsplit('"', 1)[0]
                
                decoded_value = decode_djvu_string(value)
                formatted_value = format_djvu_string(decoded_value)
                
                metadata[key] = formatted_value

            except Exception as e:
                print(f"Ошибка обработки строки: {line} | {e}")

        return metadata

    except subprocess.CalledProcessError as e:
        print("Ошибка при вызове djvused:", e)
        print(f"stderr: {e.stderr}")
        return {}

file_path = "example.djvu"
metadata = extract_djvu_metadata(file_path)

if metadata:
    print("Метаданные:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
else:
    print("Метаданные не найдены.")

result = subprocess.run(
[str(djvused_path), '-e', 'print-meta', file_path],
capture_output=True, text=True, check=True, encoding='latin1'
)
print(result.stdout)

