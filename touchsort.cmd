@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	touch "%~1"
	%SYSTEMROOT%\SysWOW64\timeout.exe /t 1 /nobreak > nul
	SHIFT
	GOTO :loop
)

@ENDLOCAL
