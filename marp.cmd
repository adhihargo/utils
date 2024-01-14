@ECHO OFF
SETLOCAL

SET MARP_PATH=D:\prog\marp

CALL npx --prefix %MARP_PATH% marp %*

ENDLOCAL
