import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from verison import EmailReceiver

@pytest.fixture
def create_email(tmp_path):
    def _create_email(text, filename="mail.txt"):
        file = tmp_path / filename
        file.write_text(text, encoding="utf-8")
        return EmailReceiver(file)
    return _create_email