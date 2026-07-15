"""Provide a deterministic AST linter for function documentation and complexity."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

MAX_FUNCTION_LINES = 30
MAX_CONTROL_FLOW_DEPTH = 4
DEFAULT_EXCLUDED_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "build",
    "dist",
    "artifacts",
}

RULE_LONG_FUNCTION = "LINT001"
RULE_CONTROL_FLOW_DEPTH = "LINT002"
RULE_MISSING_DOCSTRING = "LINT003"

CONTROL_FLOW_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.Try,
    ast.With,
    ast.AsyncWith,
    ast.Match,
)


@dataclass(frozen=True)
class WarningItem:
    """Immutable static-analysis diagnostic."""
    file_path: str
    line: int
    function_name: str
    code: str
    message: str

    def format(self) -> str:
        """Format the warning as a stable, compiler-style diagnostic line."""
        return f"{self.file_path}:{self.line}:{self.function_name}: {self.code}: {self.message}"


class _ControlFlowDepthVisitor(ast.NodeVisitor):
    """AST visitor that measures control-flow nesting within one function."""
    def __init__(self) -> None:
        """Initialize the _ControlFlowDepthVisitor."""
        self.current_depth = 0
        self.max_depth = 0

    def generic_visit(self, node: ast.AST) -> None:
        """Track control-flow depth while excluding nested function bodies."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            return

        should_count = isinstance(node, CONTROL_FLOW_NODES)
        if should_count:
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)

        super().generic_visit(node)

        if should_count:
            self.current_depth -= 1


def _iter_python_files(paths: Sequence[str], excluded_dirs: set[str]) -> Iterable[Path]:
    """Yield unique Python files while honoring excluded directory names."""
    seen: set[Path] = set()
    for raw_path in paths:
        candidate = Path(raw_path)
        if not candidate.exists():
            continue

        if candidate.is_file() and candidate.suffix == ".py":
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield resolved
            continue

        for file_path in candidate.rglob("*.py"):
            if any(part in excluded_dirs for part in file_path.parts):
                continue
            resolved = file_path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield resolved


def _function_line_count(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Return the inclusive source-line count for a function."""
    end_line = getattr(node, "end_lineno", node.lineno)
    return max(1, end_line - node.lineno + 1)


def _control_flow_depth(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Measure the maximum control-flow nesting within a function body."""
    visitor = _ControlFlowDepthVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return visitor.max_depth


def analyze_source(source: str, file_path: str = "<memory>") -> list[WarningItem]:
    """Parse Python source and report function documentation, size, and nesting violations."""
    tree = ast.parse(source)
    warnings: list[WarningItem] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        function_name = node.name
        line = node.lineno

        if ast.get_docstring(node) is None:
            warnings.append(
                WarningItem(
                    file_path=file_path,
                    line=line,
                    function_name=function_name,
                    code=RULE_MISSING_DOCSTRING,
                    message="docstring required for function",
                )
            )

        line_count = _function_line_count(node)
        if line_count > MAX_FUNCTION_LINES:
            warnings.append(
                WarningItem(
                    file_path=file_path,
                    line=line,
                    function_name=function_name,
                    code=RULE_LONG_FUNCTION,
                    message=f"function has {line_count} lines (> {MAX_FUNCTION_LINES})",
                )
            )

        depth = _control_flow_depth(node)
        if depth > MAX_CONTROL_FLOW_DEPTH:
            warnings.append(
                WarningItem(
                    file_path=file_path,
                    line=line,
                    function_name=function_name,
                    code=RULE_CONTROL_FLOW_DEPTH,
                    message=f"control flow depth {depth} (> {MAX_CONTROL_FLOW_DEPTH})",
                )
            )

    return sorted(warnings, key=lambda item: (item.file_path, item.line, item.code))


def analyze_paths(paths: Sequence[str], excluded_dirs: set[str] | None = None) -> list[WarningItem]:
    """Analyze Python files under the supplied paths and return deterministic lint warnings."""
    effective_excluded = excluded_dirs or set(DEFAULT_EXCLUDED_DIRS)
    warnings: list[WarningItem] = []

    for file_path in _iter_python_files(paths=paths, excluded_dirs=effective_excluded):
        source = file_path.read_text(encoding="utf-8")
        warnings.extend(analyze_source(source=source, file_path=str(file_path)))

    return sorted(warnings, key=lambda item: (item.file_path, item.line, item.code))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the AST linter."""
    parser = argparse.ArgumentParser(description="Static AST linter for Python functions")
    parser.add_argument("paths", nargs="+", help="File or directory paths to scan")
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude; can pass multiple times",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the AST linter command and return a process-compatible status code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS)
    excluded_dirs.update(args.exclude_dir)

    warnings = analyze_paths(paths=args.paths, excluded_dirs=excluded_dirs)
    for warning in warnings:
        print(warning.format())

    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
