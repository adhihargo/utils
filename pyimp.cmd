@ECHO OFF
SETLOCAL
SET BIN_ISORT=%PATH_PY_DEVUTILS%\Scripts\isort.exe
SET BIN_AUTOFLAKE=%PATH_PY_DEVUTILS%\Scripts\autoflake.exe

%BIN_ISORT% %*
%BIN_AUTOFLAKE% --in-place --remove-unused-variables --expand-star-imports %*
ENDLOCAL
