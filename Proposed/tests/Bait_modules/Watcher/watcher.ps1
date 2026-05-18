$FolderPath  = "C:\Program Files (x86)\sensitive"
$FolderName  = Split-Path $FolderPath -Leaf

$Query = @"
<QueryList>
  <Query Id="0" Path="Security">
    <Select Path="Security">*[System[EventID=4663]]</Select>
  </Query>
</QueryList>
"@

$LogQuery = New-Object System.Diagnostics.Eventing.Reader.EventLogQuery("Security", [System.Diagnostics.Eventing.Reader.PathType]::LogName, $Query)
$LogQuery.ReverseDirection = $false
$Watcher = New-Object System.Diagnostics.Eventing.Reader.EventLogWatcher($LogQuery)

# Record start time to file so action block can ignore old events
[datetime]::Now.ToString("yyyy-MM-dd HH:mm:ss") | Out-File "C:\watcher\starttime.log" -Force

Register-ObjectEvent -InputObject $Watcher -EventName EventRecordWritten -Action {
    try {
        $evt     = $EventArgs.EventRecord
        $xml     = [xml]$evt.ToXml()
        $object  = $xml.Event.EventData.Data | Where-Object { $_.Name -eq 'ObjectName'      } | Select-Object -ExpandProperty '#text'
        $user    = $xml.Event.EventData.Data | Where-Object { $_.Name -eq 'SubjectUserName' } | Select-Object -ExpandProperty '#text'
        $process = $xml.Event.EventData.Data | Where-Object { $_.Name -eq 'ProcessName'     } | Select-Object -ExpandProperty '#text'
        $access  = $xml.Event.EventData.Data | Where-Object { $_.Name -eq 'AccessMask'      } | Select-Object -ExpandProperty '#text'
        $time    = $evt.TimeCreated.ToString("yyyy-MM-dd HH:mm:ss")

        # Ignore events that happened before this watcher started
        $started = Get-Content "C:\watcher\starttime.log" -ErrorAction SilentlyContinue
        if ($time -lt $started) { return }


		# Production - injected by deploy.ps1
        if ($object -notlike "*FOLDER_NAME*") { return }

        # Deduplicate via file on disk - one alert per unique combination
        $key       = "$user|$object|$access|$time"
        $dedupFile = "C:\watcher\seen.log"
        $already   = Get-Content $dedupFile -ErrorAction SilentlyContinue
        if ($already -contains $key) { return }
        $key | Out-File $dedupFile -Append


        # Json Payload
        $payload = @{
            user    = $user
            path    = $object
            process = $process
            access  = $access
            event_time    = $time
        } | ConvertTo-Json

        # Production - injected by deploy.ps1
        #$url = "CALLBACK_URL?user=$user&object=$([uri]::EscapeDataString($object))&process=$([uri]::EscapeDataString($process))&access=$access&time=$([uri]::EscapeDataString($time))"

        $url = "CALLBACK_URL"

        # Local Logging
        $url      | Out-File "C:\watcher\debug.log" -Append
        
        Invoke-RestMethod -Uri $url -Method POST -Body $payload -ContentType "application/json" -TimeoutSec 5

        "SUCCESS" | Out-File "C:\watcher\debug.log" -Append

    } catch {
        $_.Exception.Message | Out-File "C:\watcher\debug.log" -Append
    }
}

$Watcher.Enabled = $true
Write-Host "[+] Watcher running - monitoring: $FolderName" -ForegroundColor Green
while ($true) { Start-Sleep -Seconds 10 }