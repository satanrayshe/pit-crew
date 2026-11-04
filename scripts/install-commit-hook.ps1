<#
.SYNOPSIS
Install a git post-commit hook that tells the herald about each commit.

.DESCRIPTION
Each commit posts "@<crew>-herald commit <short hash> <subject>" into the pit
room through scripts/pit-post.sh. Git for Windows runs hooks with its own sh
and curl, so the hook is a shell script on Windows too.

It fires for every commit in that repository, the builder's included; the
builder sees the hook and leaves the notice to it.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\install-commit-hook.ps1 -Crew pit -Repository C:\code\my-project
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z][a-z0-9-]{1,20}$')]
    [string] $Crew,

    [string] $Repository = '.'
)

$ErrorActionPreference = 'Stop'

$postScript = (Join-Path $PSScriptRoot 'pit-post.sh') -replace '\\', '/'
$hooks = git -C $Repository rev-parse --path-format=absolute --git-path hooks
if ($LASTEXITCODE -ne 0) {
    throw "$Repository is not a git repository"
}
$hook = Join-Path $hooks 'post-commit'
$marker = '# installed by pit-crew'

if ((Test-Path $hook) -and -not (Select-String -Path $hook -SimpleMatch $marker -Quiet)) {
    throw "$hook exists and was not installed by Pit Crew; leaving it alone"
}

New-Item -ItemType Directory -Force $hooks | Out-Null
$lines = @(
    '#!/bin/sh'
    $marker
    'sha=$(git rev-parse --short HEAD)'
    'subject=$(git log -1 --format=%s)'
    "`"$postScript`" `"@$Crew-herald commit `$sha `$subject`" ||"
    '  echo "pit-crew: could not tell the herald about $sha" >&2'
)
[System.IO.File]::WriteAllText($hook, ($lines -join "`n") + "`n")
Write-Host "Installed $hook. Each commit now posts `"@$Crew-herald commit <hash> <subject>`" to the room."
