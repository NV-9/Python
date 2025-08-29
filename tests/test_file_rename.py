import pytest
from pathlib import Path
from tools.file_rename import FileRenameTool


# ---------- Fixtures ----------

@pytest.fixture
def make_files(tmp_path: Path):
    """
    Factory fixture to create mock files in a temporary directory.
    Returns a function that takes a list of filenames and creates them.
    """
    def _make_files(filenames: list[str]) -> Path:
        for name in filenames:
            (tmp_path / name).write_text("dummy content")
        return tmp_path
    return _make_files


@pytest.fixture
def sample_filenames():
    """Reusable set of sample filenames."""
    return [
        "Test 01.mkv",
        "Test 02.mkv",
        "Other 03.mp4",
    ]


# ---------- Helper functions ----------

def run_tool_and_collect(source: Path, **kwargs):
    """Run FileRenameTool and return the set of resulting filenames in target directory."""
    tool = FileRenameTool(source_path=source, **kwargs)
    tool.find()
    tool.order()
    tool.rename()

    target = source if kwargs.get("in_place", False) else kwargs.get("destination_path")
    return {f.name for f in target.iterdir()}


# ---------- Tests ----------

def test_in_place_rename(make_files, sample_filenames):
    source = make_files(sample_filenames)

    results = run_tool_and_collect(
        source,
        in_place=True,
        match_regex=r"Test (\d\d)\.mkv$",
        target_regex=r"Episode \1.mkv",
    )

    assert "Episode 01.mkv" in results
    assert "Episode 02.mkv" in results
    assert not any(name.startswith("Test") for name in results)


def test_rename_to_new_directory(make_files, sample_filenames, tmp_path):
    source = make_files(sample_filenames)
    parsed_dir = tmp_path / "parsed"

    results = run_tool_and_collect(
        source,
        in_place=False,
        destination_path=parsed_dir,
        match_regex=r"Test (\d\d)\.mkv$",
        target_regex=r"Episode \1.mkv",
    )

    assert results == {"Episode 01.mkv", "Episode 02.mkv"}


def test_no_matches(make_files):
    source = make_files(["unrelated.txt"])

    results = run_tool_and_collect(
        source,
        in_place=True,
        match_regex=r"Test (\d\d)\.mkv$",
        target_regex=r"Episode \1.mkv",
    )

    assert "unrelated.txt" in results
    assert not any(name.startswith("Episode") for name in results)


def test_overwrite_behavior(make_files):
    filenames = ["Test 01.mkv", "Episode 01.mkv"]
    source = make_files(filenames)

    results = run_tool_and_collect(
        source,
        in_place=True,
        match_regex=r"Test (\d\d)\.mkv$",
        target_regex=r"Episode \1.mkv",
    )

    assert list(results).count("Episode 01.mkv") == 1


@pytest.mark.parametrize("ordering", [
    {"by_name": True},
    {"by_created_time": True},
])
def test_ordering(make_files, sample_filenames, ordering):
    source = make_files(sample_filenames)

    tool = FileRenameTool(
        source_path=source,
        in_place=True,
        match_regex=r"Test (\d\d)\.mkv$",
        target_regex=r"Episode \1.mkv",
    )
    tool.find()
    tool.order(**ordering)
    tool.rename()

    results = [f.name for f in sorted(source.iterdir())]
    assert "Episode 01.mkv" in results
    assert "Episode 02.mkv" in results
