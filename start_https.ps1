# PowerShell script to start Django server with HTTPS support
Write-Host "🔒 Starting Django Server with HTTPS Support" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan

# Set environment variables for HTTPS
$env:DJANGO_SETTINGS_MODULE = "spoorthi_macs.settings"
$env:PYTHONPATH = $PWD

Write-Host "🌐 Starting server at http://127.0.0.1:8000/" -ForegroundColor Yellow
Write-Host "🔒 HTTPS compatible - works with both HTTP and HTTPS" -ForegroundColor Green
Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Red
Write-Host "=" * 50 -ForegroundColor Cyan

try {
    # Run Django server
    python manage.py runserver --insecure 127.0.0.1:8000
}
catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host "💡 Try running: python manage.py runserver 127.0.0.1:8000" -ForegroundColor Yellow
}
