from pathlib import Path


def get_miplib_benchmark_dir() -> Path:
    # path = Path.home() / ".miplib_benchmark"
    path = Path.cwd() / ".miplib_benchmark"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_mps_files_dir() -> Path:
    path = get_miplib_benchmark_dir() / "mps_files"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_zip_path() -> Path:
    return get_miplib_benchmark_dir() / "benchmark.zip"