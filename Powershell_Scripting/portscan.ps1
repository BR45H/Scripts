param($p1)

if (!$p1){
    echo "Portscan Powershell Script"
    echo "Usage: .\portscan.ps1 <IP>"
    echo "Example: .\portscan.ps1 37.107.47.7"
} else {
    echo "Pinging host..."
    $resp = ping -n 1 "$p1" | Select-String "bytes=32"

    if ($resp){
        echo "Host $p1 is up. Scanning ports..."

        foreach ($port in 1..1024){
            $tcp = New-Object System.Net.Sockets.TcpClient
            $connection = $tcp.BeginConnect($p1, $port, $null, $null)
            $success = $connection.AsyncWaitHandle.WaitOne(200, $false)

            if ($success -and $tcp.Connected) {
                echo "Port $port is open"
            }

            $tcp.Close()
        }
    } else {
        echo "Host $p1 is down"
    }
}