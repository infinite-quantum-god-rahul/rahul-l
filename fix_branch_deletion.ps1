# Fix Branch Deletion PowerShell Script
# This script runs the direct SQLite fix to resolve FOREIGN KEY constraint errors

param(
    [Parameter(Mandatory=$false)]
    [string]$BranchCode
)

Write-Host "🔧 BRANCH DELETION FIX SCRIPT" -ForegroundColor Cyan
Write-Host "This script will directly fix your database to resolve constraint errors" -ForegroundColor Yellow
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
if (-not (Test-Path "db.sqlite3")) {
    Write-Host "❌ Database file (db.sqlite3) not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the directory containing your database file" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Database file found: db.sqlite3" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python or add it to your PATH" -ForegroundColor Red
    exit 1
}

# Check if the direct SQLite fix script exists
if (-not (Test-Path "direct_sqlite_fix.py")) {
    Write-Host "❌ Script file 'direct_sqlite_fix.py' not found" -ForegroundColor Red
    Write-Host "Please ensure all script files are in the current directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Script file found: direct_sqlite_fix.py" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 READY TO FIX BRANCH DELETION ISSUE" -ForegroundColor Green
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Connect directly to your SQLite database" -ForegroundColor White
Write-Host "  2. Find ALL tables with branch references" -ForegroundColor White
Write-Host "  3. Temporarily disable foreign key constraints" -ForegroundColor White
Write-Host "  4. Delete all related records" -ForegroundColor White
Write-Host "  5. Delete the branch itself" -ForegroundColor White
Write-Host "  6. Re-enable constraints" -ForegroundColor White
Write-Host "  7. Verify the deletion" -ForegroundColor White
Write-Host ""

Write-Host "⚠️  WARNING: This will permanently delete branch '$BranchCode' and ALL related records!" -ForegroundColor Red
Write-Host "This action cannot be undone!" -ForegroundColor Red

$confirm = Read-Host "Are you absolutely sure? Type 'YES' to proceed"
if ($confirm -ne "YES") {
    Write-Host "❌ Operation cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🔧 Starting branch deletion fix..." -ForegroundColor Cyan
Write-Host ""

# Run the Python script
try {
    $command = "python direct_sqlite_fix.py $BranchCode"
    Write-Host "Running: $command" -ForegroundColor Gray
    Write-Host ""
    
    Invoke-Expression $command
    
    Write-Host ""
    Write-Host "✅ Script execution completed" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error executing script: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Try deleting the branch again through your normal method" -ForegroundColor White
Write-Host "2. The FOREIGN KEY constraint error should no longer occur" -ForegroundColor White
Write-Host "3. If you still get errors, run this script again" -ForegroundColor White
Write-Host ""
Write-Host "✅ Branch deletion issue should now be resolved!" -ForegroundColor Green
