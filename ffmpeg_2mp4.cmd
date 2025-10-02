@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ffmpeg -i "%~1" -codec copy "%~dpn1.mp4"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
