@ECHO OFF
@SETLOCAL

IF 'x%VLC_TARGET_PORT%'=='x' (
	ECHO VLC_TARGET_PORT not defined
	PAUSE
	GOTO :exit
)

:loop
IF NOT 'x%1'=='x' (
	echo enqueue "%~1" | ncat 127.0.0.1 %VLC_TARGET_PORT% -w 1
	SHIFT
	GOTO :loop
)
:exit

@ENDLOCAL
