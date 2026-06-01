@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	rem ffmpeg -hide_banner -fflags +discardcorrupt -i "%~1" -codec copy "%~dpn1.mp4"
	ffmpeg -hide_banner -analyzeduration 100M -probesize 100M -i "%~1" -codec copy "%~dpn1.mp4"
	if ERRORLEVEL 1 GOTO skipdel
	del "%~1"
:skipdel
	SHIFT
	GOTO :loop
)

@ENDLOCAL
