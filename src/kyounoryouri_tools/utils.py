from pathlib import Path

from natsort import natsorted


def get_filepath_list(dir_path: Path, ext: str) -> list[Path]:
    """
    Get file path list with specific extension

    Args:
        dir_path (Path): directory path
        ext (str): extension

    Returns:
        list[Path]: list of file path

    """
    file_path_list = natsorted(dir_path.glob(f"*.{ext}"))
    return file_path_list
