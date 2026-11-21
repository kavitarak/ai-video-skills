# Install every skill for Claude Code, Codex, Gemini CLI and Antigravity (user level), on Windows.
# Usage: powershell -ExecutionPolicy Bypass -File install.ps1            (all tools)
#        powershell -ExecutionPolicy Bypass -File install.ps1 claude     (one tool)
param([string[]]$Tools = @("claude", "codex", "gemini", "antigravity"))
$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot ".agents\skills"
$dest = @{
  claude      = Join-Path $HOME ".claude\skills"
  codex       = Join-Path $HOME ".codex\skills"
  gemini      = Join-Path $HOME ".gemini\skills"
  antigravity = Join-Path $HOME ".gemini\config\skills"
}
foreach ($tool in $Tools) {
  if (-not $dest.ContainsKey($tool)) { throw "Unknown tool: $tool (use claude, codex, gemini or antigravity)" }
  $dir = $dest[$tool]
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  Get-ChildItem -Directory $src | ForEach-Object {
    $target = Join-Path $dir $_.Name
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $_.FullName $target
  }
  Write-Host "OK $tool -> $dir"
}
Write-Host "Done. Restart your AI tool so it picks up the new skills."
