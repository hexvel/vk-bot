import importlib
from pathlib import Path

package_path = Path(__file__).parent

module_files = [
    file.stem for file in package_path.glob("*.py") if file.name != "__init__.py"
]

admin_labelers = [
    importlib.import_module(f".{module}", __package__).labeler
    for module in module_files
]
