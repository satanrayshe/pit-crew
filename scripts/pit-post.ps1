<#
.SYNOPSIS
Post a message into the pit room through the channel's incoming webhook:
Discord, Slack or Mattermost.

.DESCRIPTION
The webhook URL comes from PIT_WEBHOOK_URL, or else DISCORD_WEBHOOK_URL (its
old name): from the environment, or else from that line of the .env file at
the top of this repository.

.EXAMPLE
powershell -ExecutionPolicy Bypass -File scripts\pit-post.ps1 -Message "@pit-scout pit check"
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $Message
)

$ErrorActionPreference = 'Stop'

$envFile = Join-Path (Split-Path -Parent $PSScriptRoot) '.env'
$url = $null
foreach ($name in 'PIT_WEBHOOK_URL', 'DISCORD_WEBHOOK_URL') {
    $url = [Environment]::GetEnvironmentVariable($name)
    if (-not $url -and (Test-Path $envFile)) {
        $line = Get-Content $envFile | Where-Object { $_ -match "^$name=" } | Select-Object -Last 1
        if ($line) {
            $url = ($line -replace "^$name=", '').Trim().Trim('"', "'")
        }
    }
    if ($url) { break }
}
if (-not $url) {
    throw "PIT_WEBHOOK_URL is not set, in the environment or in $envFile"
}
if ($url -match '^https://(discord|discordapp)\.com/api/webhooks/') {
    $field = 'content'
} elseif ($url -match '^https://hooks\.slack\.com/' -or $url -match '^https?://.+/hooks/') {
    # Slack and Mattermost both take {"text": ...}.
    $field = 'text'
} else {
    throw 'PIT_WEBHOOK_URL is not a Discord, Slack or Mattermost incoming webhook URL'
}
if (-not $Message.Trim()) {
    throw 'Nothing to post'
}

$json = @{ $field = $Message } | ConvertTo-Json -Compress
$body = [System.Text.Encoding]::UTF8.GetBytes($json)
Invoke-RestMethod -Method Post -Uri $url -ContentType 'application/json; charset=utf-8' -Body $body -TimeoutSec 15 | Out-Null
