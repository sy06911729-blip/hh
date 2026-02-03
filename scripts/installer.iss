[Setup]
AppName=Video Downloader
AppVersion=0.1.0
AppPublisher=Video Downloader
DefaultDirName={pf}\Video Downloader
DefaultGroupName=Video Downloader
OutputBaseFilename=VideoDownloaderSetup
OutputDir=dist\installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\video-downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Video Downloader"; Filename: "{app}\video-downloader.exe"
Name: "{commondesktop}\Video Downloader"; Filename: "{app}\video-downloader.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le bureau"; GroupDescription: "Raccourcis"; Flags: unchecked

[Run]
Filename: "{app}\video-downloader.exe"; Description: "Lancer Video Downloader"; Flags: nowait postinstall skipifsilent
