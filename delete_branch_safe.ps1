# Safe Branch Deletion PowerShell Script
# This script safely deletes a branch and ALL related records to prevent
# FOREIGN KEY constraint errors.

param(
    [Parameter(Mandatory=$false)]
    [string]$BranchCode,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

Write-Host "🔧 SAFE BRANCH DELETION SCRIPT" -ForegroundColor Cyan
Write-Host "This script will safely delete a branch and ALL related records" -ForegroundColor Yellow
Write-Host "to prevent FOREIGN KEY constraint errors." -ForegroundColor Yellow
Write-Host ""

# Get branch code if not provided
if (-not $BranchCode) {
    $BranchCode = Read-Host "Enter branch code to delete (e.g., BRN001)"
}

if (-not $BranchCode) {
    Write-Host "❌ No branch code provided. Exiting." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Please run this script from the Django project root directory (where manage.py is located)" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv") -and -not (Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found. Please activate your virtual environment first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} elseif (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  Virtual environment activation script not found. Please activate manually." -ForegroundColor Yellow
}

Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Build the command
$Command = "python safe_branch_deletion.py"

if ($BranchCode) {
    $Command += " $BranchCode"
}

if ($Force) {
    $Command += " --force"
}

if ($DryRun) {
    $Command += " --dry-run"
}

Write-Host "Running command: $Command" -ForegroundColor Cyan
Write-Host ""

# Execute the command
try {
    Invoke-Expression $Command
} catch {
    Write-Host "❌ Error executing command: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Script execution completed" -ForegroundColor Green
