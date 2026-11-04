# Heartbeat: a scheduled pit check

Switch has no scheduling tool. An agent wakes only when a message addresses
it. The scout recomputes the countdown from the clock every time it wakes, so
the pit board is right whenever somebody asks. A heartbeat makes it ask on its
own: every two hours it posts `@<crew>-scout pit check` into the room through
the channel's Discord webhook, and the scout updates the board and posts one
line with the countdown and the tally.

Every heartbeat starts a scout turn, which spends your coding agent's quota.
Two hours is a reasonable gap. Stop the heartbeat once the deadline passes.

## Before you schedule it

1. Create the webhook and put its URL in `.env` (step 9 of
   [docs/discord-setup.md](../docs/discord-setup.md)).
2. Post once by hand and watch the room:

   ```sh
   scripts/pit-post.sh "@pit-scout pit check"
   ```

   If the scout answers, the heartbeat will work. If the message appears but
   the scout stays quiet, the room did not let the webhook address it; see
   "Known limits" in the [README](../README.md#known-limits).

Replace `pit` with your crew name and the paths with where you cloned
pit-crew.

## macOS and Linux: cron

Run `crontab -e` and add:

```cron
0 */2 * * * /home/you/pit-crew/scripts/pit-post.sh "@pit-scout pit check" >>/tmp/pit-heartbeat.log 2>&1
```

Delete the line after the deadline.

## Windows: Task Scheduler

In PowerShell:

```powershell
$script = "$HOME\pit-crew\scripts\pit-post.ps1"
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`" -Message `"@pit-scout pit check`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration (New-TimeSpan -Days 3)
Register-ScheduledTask -TaskName 'Pit Crew heartbeat' -Action $action -Trigger $trigger
```

`-RepetitionDuration` stops it by itself after three days; set it to the time
left until your deadline. To stop it sooner:

```powershell
Unregister-ScheduledTask -TaskName 'Pit Crew heartbeat' -Confirm:$false
```

The task runs while you are signed in to Windows. `-ExecutionPolicy Bypass`
applies only to that one PowerShell process, so it can run the script on a
machine whose policy would otherwise refuse unsigned scripts.
