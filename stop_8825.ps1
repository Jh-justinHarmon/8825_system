# 8825 v3.0 - Stop All MCP Servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "8825 v3.0 - Stopping MCP Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Find and stop Python processes on MCP ports
$ports = @(8826, 8827, 8828)
$names = @("HCSS", "Team 76", "Personal")

for ($i = 0; $i -lt $ports.Count; $i++) {
    $port = $ports[$i]
    $name = $names[$i]
    
    Write-Host "Stopping $name MCP (port $port)..." -ForegroundColor Yellow
    
    # Find process using the port
    $netstatOutput = netstat -ano | Select-String ":$port.*LISTENING"
    
    if ($netstatOutput) {
        $processId = ($netstatOutput -split '\s+')[-1]
        
        try {
            Stop-Process -Id $processId -Force
            Write-Host "  ✓ Stopped process $processId" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Failed to stop process $processId" -ForegroundColor Red
        }
    } else {
        Write-Host "  - No process found on port $port" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All MCP Servers Stopped" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
