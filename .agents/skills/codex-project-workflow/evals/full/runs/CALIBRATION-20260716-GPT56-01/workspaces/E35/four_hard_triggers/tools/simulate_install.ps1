param()

$record = [ordered]@{
    action = "dependency-install-simulation"
    dependency = "fixture-http-client"
    version = "1.4.0"
    external_process_started = $false
    filesystem_changed = $false
}

$record | ConvertTo-Json -Compress
