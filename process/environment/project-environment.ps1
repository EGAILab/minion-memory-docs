# Minion-Memory project environment (Owner rule OWN-001, 2026-10-09):
# every project-controlled temporary file, cache, build output and review worktree lives on E:
# inside the Minion-Memory project folder. Never on C:.
#
# Dot-source in every shell that may create temp/cache files:
#   . E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory-docs\process\environment\project-environment.ps1
# This changes only the current process environment, never Windows user/system settings.

$MnemeRoot = 'E:\AI\Projects\OpenMinds\Minions\Minion-Memory'
$MnemeTmp  = Join-Path $MnemeRoot '.tmp'
$MnemeCache = Join-Path $MnemeTmp 'cache'

foreach ($dir in @("$MnemeTmp\process-temp", $MnemeCache, "$MnemeTmp\work", "$MnemeRoot\review-worktrees")) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
}

$env:TEMP = "$MnemeTmp\process-temp"
$env:TMP = "$MnemeTmp\process-temp"
$env:TMPDIR = "$MnemeTmp\process-temp"
$env:UV_CACHE_DIR = "$MnemeCache\uv"
$env:UV_PYTHON_INSTALL_DIR = "$MnemeCache\uv-python"
$env:PIP_CACHE_DIR = "$MnemeCache\pip"
$env:PYTHONPYCACHEPREFIX = "$MnemeCache\pycache"
$env:RUFF_CACHE_DIR = "$MnemeCache\ruff"
$env:MYPY_CACHE_DIR = "$MnemeCache\mypy"
$env:HYPOTHESIS_STORAGE_DIRECTORY = "$MnemeCache\hypothesis"
$env:CARGO_TARGET_DIR = "$MnemeCache\cargo-target\windows"
# Cargo registry/git caches (NF-023); the rustup toolchains already installed on C: are executed only.
$env:CARGO_HOME = "$MnemeCache\cargo-home"
# Project-local interpreter (NF-023): uv-managed CPython 3.12.8 under UV_PYTHON_INSTALL_DIR,
# never a system Python. Install new interpreters only with `uv python install --no-bin`.
$env:UV_PYTHON_PREFERENCE = 'only-managed'
$env:UV_PYTHON = '3.12.8'
$env:MNEME_PYTEST_CACHE = "$MnemeCache\pytest"
# Language environments created by uv for the repos (outside the repo trees):
$env:MNEME_VENV_ROOT = "$MnemeCache\venvs"
