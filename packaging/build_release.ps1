# Build a Windows installer that already contains Python deps + FFmpeg.
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$Vendor = Join-Path $Root "vendor\ffmpeg"
New-Item -ItemType Directory -Force -Path $Vendor | Out-Null

function Get-FFmpeg {
    $ff = Join-Path $Vendor "ffmpeg.exe"
    $fp = Join-Path $Vendor "ffprobe.exe"
    if ((Test-Path $ff) -and (Test-Path $fp)) {
        Write-Host "Using bundled FFmpeg in vendor\ffmpeg"
        return
    }
    $zip = Join-Path $Root "vendor\ffmpeg-release-essentials.zip"
    $url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    Write-Host "Downloading FFmpeg essentials..."
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    $extract = Join-Path $Root "vendor\_ffmpeg_extract"
    if (Test-Path $extract) { Remove-Item -Recurse -Force $extract }
    Expand-Archive -LiteralPath $zip -DestinationPath $extract -Force
    $bin = Get-ChildItem -Path $extract -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
    if (-not $bin) { throw "ffmpeg.exe not found in essentials zip" }
    Copy-Item (Join-Path $bin.DirectoryName "ffmpeg.exe") $ff -Force
    Copy-Item (Join-Path $bin.DirectoryName "ffprobe.exe") $fp -Force
    Remove-Item -Recurse -Force $extract
    Remove-Item -Force $zip
    Write-Host "FFmpeg copied to vendor\ffmpeg"
}

Get-FFmpeg

Write-Host "Installing PyInstaller if needed..."
python -m pip install --upgrade pip pyinstaller
Write-Host "Building app..."
python -m PyInstaller --noconfirm --clean 11_converter.spec

$iscc = @(
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { throw "Inno Setup compiler not found. Install JRSoftware.InnoSetup." }

Write-Host "Building installer..."
& $iscc (Join-Path $Root "packaging\11_converter.iss")
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed: $LASTEXITCODE" }

$setup = Join-Path $Root "dist\11_CONVERTER_Setup.exe"
if (-not (Test-Path $setup)) { throw "Installer not created: $setup" }
Write-Host "Installer ready: $setup"
