; Sistema de Gestion para Librerias - Inno Setup Script

#define AppName      "Sistema de Gestion para Librerias"
#define AppVersion   "1.0.0"
#define AppPublisher "Tu Nombre o Empresa"
#define AppExeName   "SistemaLibreria.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\SistemaLibreria
DefaultGroupName={#AppName}
AllowNoIcons=yes
OutputDir=..\output_instalador
OutputBaseFilename=Instalador_SistemaLibreria_v{#AppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "..\dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\data\catalogo.db";   DestDir: "{app}\data"; Flags: ignoreversion onlyifdoesntexist
Source: "..\data\ventas.db";     DestDir: "{app}\data"; Flags: ignoreversion onlyifdoesntexist

[Dirs]
Name: "{app}\assets"
Name: "{app}\data"

[Icons]
Name: "{group}\{#AppName}";             Filename: "{app}\{#AppExeName}"
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}";       Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Abrir ahora"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data"
Type: filesandordirs; Name: "{app}\assets"

[Code]
function InitializeSetup(): Boolean;
var
  ExePath: String;
begin
  ExePath := ExpandConstant('{src}\..\dist\{#AppExeName}');
  if not FileExists(ExePath) then
  begin
    MsgBox(
      'No se encontro el ejecutable.' + #13#10 +
      'Ejecuta build.bat primero y luego vuelve a abrir este instalador.',
      mbError, MB_OK
    );
    Result := False;
  end else
    Result := True;
end;
