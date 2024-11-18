@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ffmpeg -i "%~1" -map 0:0 -codec copy "%~n1-%~x1"
	nircmd clonefiletime %1 "%~n1-%~x1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
