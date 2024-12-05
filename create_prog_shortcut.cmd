@ECHO OFF
@SETLOCAL

REM Depends on wnd32 git's create-shortcut.exe.
IF NOT 'x%PROG_PATH%'=='' (
	SET PROG_PATH=C:\prog
)

:loop
IF NOT 'x%1'=='x' (
	for %%y in ("%~dp1\.") do echo %%~nxy
	start create-shortcut "%~1" "%PROG_PATH%\%~n1.lnk"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
