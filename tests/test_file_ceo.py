from hackaton.version import FileCEO

def test_move_file(tmp_path):
    source = tmp_path / "mail.txt"
    source.write_text("hello", encoding="utf-8")
    out_dir = tmp_path / "outbox"
    manager = FileCEO(out_dir)
    manager.move_file(source, "spam")
    moved = out_dir / "spam" / "mail.txt"
    assert moved.exists()
