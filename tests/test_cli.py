"""Test the minimal CLI."""

from json import dumps
from tempfile import NamedTemporaryFile

from multihash.cli import build_parser, compute, print_results


def test_json_output(capsys):  # or use "capfd" for fd-level
    """Test the output function prints JSON as expected."""
    print_results({"foo": "bar"})
    captured = capsys.readouterr()
    assert captured.out == dumps({"foo": "bar"}, indent=2) + "\n"


def test_parser_builds():
    """Test building the parser doesn't raise errors."""
    build_parser()


def test_compute():
    """Test the computation the CLI does."""
    tmp_name = None  # So we have it outside the context manager.
    with NamedTemporaryFile() as temp:
        tmp_name = temp.name
        temp.write(b"This is some test data.\n")
        temp.seek(0)
        result = compute([temp.name], ["md5", "sha256"], 512)
    assert (
        result[tmp_name]["sha256"]
        == "524d7edddd0f6e364120af132ce1100d4200246aecb2540519d8280c648f026b"
    )
    assert result[tmp_name]["md5"] == "6108e0aae2f7a4d18da546f3c66d23b0"
