from pathlib import Path
import requests
import chardet


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_PATH = RAW_DATA_DIR / "Athlete_Non-Athlete.csv"

FIGSHARE_ARTICLE_ID = "13035050"
FIGSHARE_API_URL = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"


def detect_file_encoding(file_path: Path, n_bytes: int = 10000) -> dict:
    with open(file_path, "rb") as rawdata:
        result = chardet.detect(rawdata.read(n_bytes))
    return result


def get_figshare_file_info() -> dict:
    response = requests.get(FIGSHARE_API_URL, timeout=30)
    response.raise_for_status()

    article_metadata = response.json()
    files = article_metadata.get("files", [])

    if not files:
        raise ValueError("no files found for the figshare article")

    # prefer the csv file if multiple files are present
    csv_file = next(
        (
            file_info
            for file_info in files
            if file_info.get("name", "").lower().endswith(".csv")
        ),
        None,
    )

    if csv_file is None:
        raise ValueError("no csv file found in the figshare article")

    return csv_file


def download_file(download_url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(download_url, stream=True, timeout=60) as response:
        response.raise_for_status()

        with open(output_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    output_file.write(chunk)


def main():
    file_info = get_figshare_file_info()
    download_url = file_info.get("download_url")

    if not download_url:
        raise ValueError("download_url not found in figshare file metadata")

    download_file(download_url, RAW_DATA_PATH)

    encoding_info = detect_file_encoding(RAW_DATA_PATH)

    print(f"downloaded: {RAW_DATA_PATH}")
    print(f"source file: {file_info.get('name')}")
    print(f"encoding detection: {encoding_info}")


if __name__ == "__main__":
    main()