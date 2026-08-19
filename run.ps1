$ErrorActionPreference = "Stop"
$workspaceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $workspaceRoot ".venv\Scripts\python.exe"
$bundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = "py"
} elseif ((Get-Command python -ErrorAction SilentlyContinue) -and -not (Test-Path -LiteralPath $bundledPython)) {
    $pythonExe = "python"
} elseif (Test-Path -LiteralPath $bundledPython) {
    $pythonExe = $bundledPython
} else {
    throw "No usable Python interpreter found. Install Python 3.12 or create .venv."
}

$env:PYTHONUTF8 = "1"
if (-not $env:ARK_MVP_HOST) {
    $env:ARK_MVP_HOST = "0.0.0.0"
}
Set-Location -LiteralPath $workspaceRoot
& $pythonExe app.py
