<#
.SYNOPSIS
Post a message into the pit room through a Discord webhook.

.DESCRIPTION
The webhook URL comes from DISCORD_WEBHOOK_URL, or else from the
DISCORD_WEBHOOK_URL line of the .env file at the top of this repository.

.EXAMPLE
scripts\pit-post.ps1 -Message "@pit-scout pit check"
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $Message
)

$ErrorActionPreference = 'Stop'

$url = $env:DISCORD_WEBHOOK_URL
$envFile = Join-Path (Split-Path -Parent $PSScriptRoot) '.env'
if (-not $url -and (Test-Path $envFile)) {
    $line = Get-Content $envFile | Where-Object { $_ -match '^DISCORD_WEBHOOK_URL=' } | Select-Object -Last 1
    if ($line) {
        $url = ($line -replace '^DISCORD_WEBHOOK_URL=', '').Trim().Trim('"', "'")
    }
}
if (-not $url) {
    throw "DISCORD_WEBHOOK_URL is not set, in the environment or in $envFile"
}
if ($url -notmatch '^https://(discord|discordapp)\.com/api/webhooks/') {
    throw 'DISCORD_WEBHOOK_URL is not a Discord webhook URL'
}
if (-not $Message.Trim()) {
    throw 'Nothing to post'
}

$json = @{ content = $Message } | ConvertTo-Json -Compress
$body = [System.Text.Encoding]::UTF8.GetBytes($json)
Invoke-RestMethod -Method Post -Uri $url -ContentType 'application/json; charset=utf-8' -Body $body -TimeoutSec 15 | Out-Null
