@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ffmpeg -i "%~1" -map 0:1 -codec copy -f adts "%~dpn1.aac"
	nircmd clonefiletime "%~1" "%~dpn1.aac"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
