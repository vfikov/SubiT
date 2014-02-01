; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D7089605-FCB7-4BEA-AE62-AFF97BC60283}
AppName=SubiT
AppVersion=|$#VERSION#$|
AppVerName=SubiT |$#VERSION#$|
AppPublisher=SubiT
AppPublisherURL=http://www.subit-app.sf.net/
AppSupportURL=http://www.subit-app.sf.net/
AppUpdatesURL=http://www.subit-app.sf.net/
ArchitecturesInstallIn64BitMode=x64 ia64
ChangesAssociations=yes
CloseApplications=yes
RestartApplications=yes
ChangesEnvironment=yes
SetupIconFile=|$#ROOTDIR#$|\build\setup\win32\_helpers\subit-icon-setup.ico
SolidCompression=True
ShowLanguageDialog=no
VersionInfoVersion=|$#VERSION#$|
VersionInfoCompany=SubiT
VersionInfoDescription=SubiT - Download subtitles with just one click
VersionInfoTextVersion=|$#VERSION#$|
VersionInfoProductName=SubiT
VersionInfoProductVersion=|$#VERSION#$|
VersionInfoProductTextVersion=|$#VERSION#$|
InternalCompressLevel=ultra
CompressionThreads=2
WizardSmallImageFile=|$#ROOTDIR#$|\build\setup\win32\_helpers\subit-logo-setup.bmp
WizardImageFile=|$#ROOTDIR#$|\build\setup\win32\_helpers\subit-image-setup.bmp
WizardImageStretch=False
UninstallDisplayName=SubiT
UninstallDisplayIcon={app}\SubiT.exe
DefaultDirName={userappdata}\SubiT
DisableDirPage=yes
DefaultGroupName=SubiT
DisableProgramGroupPage=yes
UsePreviousAppDir=False
PrivilegesRequired=none

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]

[InstallDelete]
Type: files; Name: "{app}\settings\config.ini"
Type: files; Name: "{uninstallexe}"


[Files]
Source: "|$#ROOTDIR#$|\build\bin\win32\|$#VERSION#$|\debug\*"; DestDir: "{userappdata}\SubiT"; Flags: ignoreversion createallsubdirs recursesubdirs
; NOTE Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\SubiT"; Filename: "{app}\SubiT.exe"
Name: "{group}\{cm:ProgramOnTheWeb,SubiT}"; Filename: "http://www.subit-app.sf.net/"
Name: "{group}\{cm:UninstallProgram,SubiT}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\SubiT"; Filename: "{app}\SubiT.exe";

[Run]
Filename: "{app}\SubiT.exe"; Parameters: "-associate"; WorkingDir: "{app}"; Flags: postinstall waituntilterminated; Description: "Associate SubiT with video files extensions"
Filename: "{app}\SubiT.exe"; Flags: nowait postinstall skipifsilent; Description: "{cm:LaunchProgram,SubiT}"

[UninstallRun]
Filename: "{app}\SubiT.exe"; Parameters: "-disassociate"; WorkingDir: "{app}"; Flags: waituntilterminated