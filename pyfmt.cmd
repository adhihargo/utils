@ECHO OFF
SETLOCAL
SET BIN_YAPF=C:\prog\venv\312_devutils\Scripts\yapf.exe

%BIN_YAPF% -i --style %~dp0\yapf_style.cfg %*
ENDLOCAL
