@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ffmpeg -hide_banner -i "%~1" -codec copy -metadata:s:v rotate="90" "%~dpn1_rot%~x1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
