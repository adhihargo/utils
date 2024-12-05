@ECHO OFF
SETLOCAL
SET BIN_ISORT=C:\prog\venv\312_devutils\Scripts\isort.exe
SET BIN_AUTOFLAKE=C:\prog\venv\312_devutils\Scripts\autoflake.exe

%BIN_ISORT% %*
%BIN_AUTOFLAKE% --in-place --remove-unused-variables --expand-star-imports %*
ENDLOCAL
