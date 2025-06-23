from src.data import commands

def test_load_csv_reads_file(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("a,b,c\n1,2,3\n")
    rows = commands.load_csv(str(file))
    assert rows == [["a", "b", "c"], ["1", "2", "3"]]

def test_init_replies_loads_data(monkeypatch):
    # Patch load_csv to return predictable data
    monkeypatch.setattr(commands, "load_csv", lambda x: [["cat", "cmd", "rep"]] if "input" in x else [["q", "a"]])
    commands.init_replies()
    assert "cat" in commands.commands
    assert "cat" in commands.replies
    assert "q" in commands.q_and_a