# Packaging 11 CONVERTER

Users should not need Python or FFmpeg. The official Windows installer
bundles the app **and** FFmpeg.

## Build the installer

From the project root (Windows):

```text
winget install --id JRSoftware.InnoSetup -e --accept-package-agreements --accept-source-agreements
powershell -ExecutionPolicy Bypass -File packaging\build_release.ps1
```

Output: `dist/11_CONVERTER_Setup.exe`

The script downloads the Gyan FFmpeg essentials build into `vendor/ffmpeg/`
(gitignored), then runs PyInstaller (folder build) and Inno Setup.

## Publish a GitHub Release

```text
gh release create v1.1.0 dist/11_CONVERTER_Setup.exe --title "11 CONVERTER 1.1.0" --notes "Windows installer. No Python or FFmpeg setup required."
```

## Notes

- The installer writes to `%LOCALAPPDATA%\11 CONVERTER` and does not need Administrator.
- FFmpeg is GPL; see `packaging/NOTICE_FFMPEG.txt`.
- Unsigned builds may show a SmartScreen warning. That is expected.
