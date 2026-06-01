from hackaton.version import FileCEO

def test_move_file(tmp_path):
    source = tmp_path / "mail.txt"
    source.write_text("hello", encoding="utf-8")
    out_dir = tmp_path / "outbox"
    manager = FileCEO(out_dir)
    result_path = manager.move_file(source, "spam")
    expected_path = out_dir / "spam" / "mail.txt"
    assert expected_path.exists()
    assert expected_path.read_text(encoding="utf-8") == "hello"
    assert result_path == expected_path
