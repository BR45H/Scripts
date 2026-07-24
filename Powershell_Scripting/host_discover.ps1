#Ping Sweep
param($p1)
if (!$p1){
	echo "Ping Powershell script"
	echo "Usage: .\host_discover.ps1 <Network>"
	echo "Example: .\host_discover.ps1 192.168.10"
} else {
    foreach ($ip in 1..254){
        $resp = ping -n 1 "$p1.$ip" | Select-String "bytes=32"
        if ($resp) {
            $activeip = $resp.Line.split(' ')[2] -replace ":", ""
            echo "Host: $activeip is online"
        }
    }
}