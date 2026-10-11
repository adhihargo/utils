@ECHO OFF
@SETLOCAL

GOTO :loopstart
:loop
%SYSTEMROOT%\SysWOW64\timeout.exe /t 1 /nobreak > nul
:loopstart
IF NOT 'x%1'=='x' (
	touch "%~1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
