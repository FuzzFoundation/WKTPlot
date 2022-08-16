from pathlib import Path
import os


SOURCE_PATH = (Path(__file__).parent / ".." / ".." / "src" / "wktplot").resolve()


class TestFolderStructure:
    def test_source_structure_has_init_files(self):
        assert SOURCE_PATH.is_dir()
        for directory, _, files in os.walk(SOURCE_PATH):
            directory = Path(directory)
            if directory.name == "__pycache__":
                continue
            assert "__init__.py" in files, f"Folder missing __init__.py file, {directory}"
