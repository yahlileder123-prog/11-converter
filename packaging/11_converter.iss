#define MyAppName "11 CONVERTER"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "11 CONVERTER"
#define MyAppURL "https://github.com/yahlileder123-prog/11-converter"
#define MyAppExeName "11_CONVERTER.exe"

[Setup]
AppId={{8F3C11A0-11C0-4A11-9C11-11C0A11E1101}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={localappdata}\11 CONVERTER
DefaultGroupName=11 CONVERTER
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=11_CONVERTER_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupLogging=no
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
LicenseFile=NOTICE_FFMPEG.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\11_CONVERTER\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "NOTICE_FFMPEG.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\11 CONVERTER"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\11 CONVERTER"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch 11 CONVERTER"; Flags: nowait postinstall skipifsilent
