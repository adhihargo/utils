@ECHO OFF
@SETLOCAL

REM Depends on wnd32 git's create-shortcut.exe.
IF NOT 'x%PROG_PATH%'=='' (
	SET PROG_PATH=C:\prog
)

:loop
IF NOT 'x%1'=='x' (
	ECHO @REM Created with create_prog_batch > "%PROG_PATH%\%~n1.cmd"
	ECHO @ECHO OFF		>> "%PROG_PATH%\%~n1.cmd"
	ECHO %1 %%*		>> "%PROG_PATH%\%~n1.cmd"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
