from src.data.utils import remove_duplicate_lines

def test_remove_duplicate_lines(tmp_path):
    file = tmp_path / "dupes.txt"
    file.write_text("a\nb\na\n")
    remove_duplicate_lines(str(file))
    lines = file.read_text().splitlines()
    assert sorted(lines) == ["a", "b"]
