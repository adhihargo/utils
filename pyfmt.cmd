@ECHO OFF
SETLOCAL
SET BIN_YAPF=%PATH_PY_DEVUTILS%\Scripts\yapf.exe

%BIN_YAPF% -i --style %~dp0\yapf_style.cfg %*
ENDLOCAL
