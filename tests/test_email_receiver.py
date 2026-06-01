from verison import EmailReceiver

def test_read_valid_text_file(tmp_path):
    file = tmp_path / "mail.txt"
    file.write_text("Привет", encoding="utf-8")
    email = EmailReceiver(file)
    assert email.is_good is True
    assert email.content == "привет"

def test_binary_file_marked_as_bad(tmp_path):
    file = tmp_path / "virus.exe"
    file.write_text("binary")
    email = EmailReceiver(file)
    assert email.is_good is False

def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")
    email = EmailReceiver(file)
    assert email.textpreprocessing() == []