@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ffprobe -hide_banner "%~1" 2>&1 | sed --quiet -e "/\(Input\|Stream\) #/p" -e "/\(Duration\):/p"
	SHIFT
	GOTO :loop
)
pause

@ENDLOCAL
