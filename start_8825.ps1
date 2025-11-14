# 8825 v3.0 - Windows Startup Script
# Installs Python, sets up venv, installs dependencies, starts all MCP servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "8825 v3.0 - Windows Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$BASE_DIR = $PSScriptRoot

# Check if Python is installed
Write-Host "Checking for Python..." -ForegroundColor Yellow
$pythonCmd = $null

# Try different Python commands
$pythonCommands = @("python", "python3", "py")
foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = $cmd
            Write-Host "  ✓ Found: $version" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

# If Python not found, provide installation instructions
if (-not $pythonCmd) {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Python Installation Required:" -ForegroundColor Yellow
    Write-Host "  1. Download Python from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  2. Run installer and CHECK 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  3. Restart PowerShell and run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Quick Install (winget):" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3.12" -ForegroundColor White
    Write-Host ""
    
    # Try to install via winget if available
    try {
        $wingetCheck = & winget --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Attempting automatic installation via winget..." -ForegroundColor Yellow
            $response = Read-Host "Install Python 3.12 now? (y/n)"
            if ($response -eq "y") {
                & winget install Python.Python.3.12 --silent
                Write-Host ""
                Write-Host "Python installed! Please restart PowerShell and run this script again." -ForegroundColor Green
                exit 0
            }
        }
    } catch {
        # winget not available
    }
    
    exit 1
}

# Check/create virtual environment
Write-Host ""
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
$venvPath = Join-Path $BASE_DIR ".venv"

if (-not (Test-Path (Join-Path $venvPath "Scripts\python.exe"))) {
    Write-Host "  Creating new virtual environment..." -ForegroundColor White
    & $pythonCmd -m venv $venvPath
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  ✓ Virtual environment exists" -ForegroundColor Green
}

# Activate virtual environment
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
Write-Host "  Activating virtual environment..." -ForegroundColor White
& $activateScript

# Install/upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
$requirementsPath = Join-Path $BASE_DIR "requirements.txt"

if (Test-Path $requirementsPath) {
    & pip install -r $requirementsPath --quiet
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found!" -ForegroundColor Red
    exit 1
}

# Check for .env files
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
$envIssues = @()

$focusDirs = @("hcss", "joju", "jh_assistant")
foreach ($focus in $focusDirs) {
    $envPath = Join-Path $BASE_DIR "focuses\$focus\mcp_server\.env"
    if (-not (Test-Path $envPath)) {
        $envIssues += $focus
    }
}

if ($envIssues.Count -gt 0) {
    Write-Host "  ⚠ Missing .env files for: $($envIssues -join ', ')" -ForegroundColor Yellow
    Write-Host "  Servers will start but may need configuration" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ All .env files present" -ForegroundColor Green
}

# Start MCP servers
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting MCP Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start HCSS MCP (port 8826)
Write-Host "Starting HCSS MCP (port 8826)..." -ForegroundColor Yellow
$hcssPath = Join-Path $BASE_DIR "focuses\hcss\mcp_server"
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory $hcssPath -WindowStyle Hidden
Start-Sleep -Milliseconds 500
Write-Host "  ✓ HCSS MCP started" -ForegroundColor Green

# Start Team 76 MCP (port 8827)
Write-Host "Starting Team 76 MCP (port 8827)..." -ForegroundColor Yellow
$jojuPath = Join-Path $BASE_DIR "focuses\joju\mcp_server"
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory $jojuPath -WindowStyle Hidden
Start-Sleep -Milliseconds 500
Write-Host "  ✓ Team 76 MCP started" -ForegroundColor Green

# Start Personal MCP (port 8828)
Write-Host "Starting Personal MCP (port 8828)..." -ForegroundColor Yellow
$jhPath = Join-Path $BASE_DIR "focuses\jh_assistant\mcp_server"
Start-Process -FilePath "python" -ArgumentList "server.py" -WorkingDirectory $jhPath -WindowStyle Hidden
Start-Sleep -Milliseconds 500
Write-Host "  ✓ Personal MCP started" -ForegroundColor Green

# Wait for servers to initialize
Write-Host ""
Write-Host "Waiting for servers to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Test server health
Write-Host ""
Write-Host "Testing server health..." -ForegroundColor Yellow

$ports = @(8826, 8827, 8828)
$names = @("HCSS", "Team 76", "Personal")
$allHealthy = $true

for ($i = 0; $i -lt $ports.Count; $i++) {
    $port = $ports[$i]
    $name = $names[$i]
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/health" -TimeoutSec 2 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ $name MCP (port $port) - healthy" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $name MCP (port $port) - unhealthy" -ForegroundColor Red
            $allHealthy = $false
        }
    } catch {
        Write-Host "  ✗ $name MCP (port $port) - not responding" -ForegroundColor Red
        $allHealthy = $false
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "8825 v3.0 Startup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($allHealthy) {
    Write-Host "All MCP servers are running!" -ForegroundColor Green
} else {
    Write-Host "Some servers failed to start. Check logs for details." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Access URLs:" -ForegroundColor White
Write-Host "  HCSS MCP:    http://localhost:8826" -ForegroundColor Cyan
Write-Host "  Team 76 MCP: http://localhost:8827" -ForegroundColor Cyan
Write-Host "  Personal MCP: http://localhost:8828" -ForegroundColor Cyan
Write-Host ""
Write-Host "Health Checks:" -ForegroundColor White
Write-Host "  curl http://localhost:8826/health" -ForegroundColor Gray
Write-Host "  curl http://localhost:8827/health" -ForegroundColor Gray
Write-Host "  curl http://localhost:8828/health" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop servers: Run stop_8825.ps1" -ForegroundColor White
Write-Host ""
