# Simple Git Push Script
# Run this script with Administrator privileges

Write-Host "Starting Git setup and push..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed. Please install from: https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "After installing Git, run this script again." -ForegroundColor Yellow
    exit 1
}

# Configure Git if not configured
Write-Host "Configuring Git..." -ForegroundColor Cyan

$userName = git config --global user.name
$userEmail = git config --global user.email

if (-not $userName) {
    Write-Host "Please enter your name for Git:" -ForegroundColor Yellow
    $name = Read-Host
    git config --global user.name $name
}

if (-not $userEmail) {
    Write-Host "Please enter your email for Git:" -ForegroundColor Yellow
    $email = Read-Host
    git config --global user.email $email
}

Write-Host "Git configured successfully!" -ForegroundColor Green

# Check if Git repository exists
if (Test-Path ".git") {
    Write-Host "Git repository already exists!" -ForegroundColor Green
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    git init
    Write-Host "Git repository initialized!" -ForegroundColor Green
}

# Add all files to staging
Write-Host "Adding files to Git..." -ForegroundColor Cyan
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Cyan
git commit -m "Fix admin_users endpoint and add user management features"

Write-Host "Changes committed successfully!" -ForegroundColor Green

# Check if remote origin exists
$remoteOrigin = git remote get-url origin 2>$null

if ($remoteOrigin) {
    Write-Host "Remote origin exists: $remoteOrigin" -ForegroundColor Green
} else {
    Write-Host "Please enter GitHub repository URL:" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/username/TOOLS-DEMO.git" -ForegroundColor Gray
    $repoUrl = Read-Host
    git remote add origin $repoUrl
    Write-Host "Remote origin added!" -ForegroundColor Green
}

# Push code to GitHub
Write-Host "Pushing code to GitHub..." -ForegroundColor Cyan
try {
    git push -u origin main
    Write-Host "Code pushed successfully!" -ForegroundColor Green
} catch {
    try {
        git push -u origin master
        Write-Host "Code pushed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "Failed to push code. Possible reasons:" -ForegroundColor Red
        Write-Host "   - No access to repository" -ForegroundColor Red
        Write-Host "   - Not logged in to GitHub" -ForegroundColor Red
        Write-Host "   - Incorrect repository URL" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manual instructions:" -ForegroundColor Yellow
        Write-Host "1. Open GitHub and create new repository" -ForegroundColor White
        Write-Host "2. Copy repository URL" -ForegroundColor White
        Write-Host "3. Run: git remote add origin <URL>" -ForegroundColor White
        Write-Host "4. Run: git push -u origin main" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "COMPLETED!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Git has been installed and configured" -ForegroundColor Green
Write-Host "Code has been committed and pushed to GitHub" -ForegroundColor Green
Write-Host "Render will automatically redeploy with new code" -ForegroundColor Green
Write-Host ""
Write-Host "Sample accounts for testing:" -ForegroundColor Cyan
Write-Host "   - Admin: admin / admin123" -ForegroundColor White
Write-Host "   - Manager: manager / manager123" -ForegroundColor White
Write-Host "   - Sales: sales1 / sales123" -ForegroundColor White
Write-Host "   - Technician: tech1 / tech123" -ForegroundColor White

Read-Host "Press Enter to exit"
