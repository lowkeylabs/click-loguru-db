from click.testing import CliRunner
from src import _main

def test_check_empty_call():
    runner = CliRunner()
    result = runner.invoke(_main.cli)
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "  build" in result.output
    assert "  deploy" in result.output
    assert "  check" in result.output

def test_check_deploy_help():
    runner = CliRunner()
    result = runner.invoke(_main.cli,["deploy","--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
