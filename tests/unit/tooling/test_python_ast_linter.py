from __future__ import annotations

from pathlib import Path

from tooling.python_ast_linter import (
    RULE_CONTROL_FLOW_DEPTH,
    RULE_LONG_FUNCTION,
    RULE_MISSING_DOCSTRING,
    analyze_paths,
    analyze_source,
    main,
)


def _codes(warnings):
    return {warning.code for warning in warnings}


def test_missing_docstring_warning() -> None:
    warnings = analyze_source("def no_docs():\n    return 1\n", file_path="example.py")
    assert RULE_MISSING_DOCSTRING in _codes(warnings)


def test_function_line_limit_warning() -> None:
    source = "def many_lines():\n    \"doc\"\n" + "\n".join(["    x = 1"] * 31) + "\n"
    warnings = analyze_source(source, file_path="example.py")
    assert RULE_LONG_FUNCTION in _codes(warnings)


def test_control_flow_depth_warning() -> None:
    source = """def deep():
    \"doc\"
    if True:
        for _ in range(1):
            while False:
                with open(\"x\"):
                    if True:
                        return 1
"""
    warnings = analyze_source(source, file_path="example.py")
    assert RULE_CONTROL_FLOW_DEPTH in _codes(warnings)


def test_cli_exit_code_non_zero_on_warnings(tmp_path: Path, capsys) -> None:
    file_path = tmp_path / "bad.py"
    file_path.write_text("def no_docs():\n    return 1\n", encoding="utf-8")

    exit_code = main([str(file_path)])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert f"{file_path}:1:no_docs:" in output


def test_cli_respects_default_exclusions(tmp_path: Path) -> None:
    excluded_dir = tmp_path / "artifacts"
    excluded_dir.mkdir(parents=True)
    (excluded_dir / "skip.py").write_text("def no_docs():\n    return 1\n", encoding="utf-8")

    warnings = analyze_paths([str(tmp_path)])
    assert not warnings
