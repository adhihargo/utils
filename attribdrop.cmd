@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	ECHO Attribute drop: "%~1"
	attrib -r -h -s "%~1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
