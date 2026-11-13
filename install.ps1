# Install apple-hig-live for Claude Code, Codex, Antigravity 2.0, Gemini CLI, Cursor.
# Usage: .\install.ps1 [-Target claude|codex|antigravity|gemini|cursor|all] [-Scope user|project]
param(
  [ValidateSet("claude", "codex", "antigravity", "gemini", "cursor", "all")][string]$Target = "all",
  [ValidateSet("user", "project")][string]$Scope = "user"
)
$ErrorActionPreference = "Stop"

$Src = Join-Path $PSScriptRoot "skills\apple-hig-live"
if (-not (Test-Path $Src)) { throw "skill folder not found: $Src" }

function Get-Dest([string]$t) {
  if ($Scope -eq "project") {
    switch ($t) {
      "claude"      { return ".claude\skills" }
      "codex"       { return ".codex\skills" }
      "antigravity" { return ".agents\skills" }
      "gemini"      { return ".gemini\skills" }
      "cursor"      { return ".cursor\skills" }
    }
  } else {
    switch ($t) {
      "claude"      { return Join-Path $HOME ".claude\skills" }
      "codex"       { return Join-Path $HOME ".codex\skills" }
      "antigravity" { return Join-Path $HOME ".gemini\config\skills" }
      "gemini"      { return Join-Path $HOME ".gemini\skills" }
      "cursor"      { return Join-Path $HOME ".cursor\skills" }
    }
  }
}

function Install-One([string]$t) {
  $dest = Get-Dest $t
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  $target = Join-Path $dest "apple-hig-live"
  if (Test-Path $target) { Remove-Item -Recurse -Force $target }
  Copy-Item -Recurse $Src $target
  Write-Host " [OK] Installed apple-hig-live for $t -> $target" -ForegroundColor Green
}

if ($Target -eq "all") {
  "claude", "codex", "antigravity", "gemini", "cursor" | ForEach-Object { Install-One $_ }
} else {
  Install-One $Target
}
