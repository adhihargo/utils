@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	qpdf -qdf %1 "%~dpn1.qdf"
	nircmd clonefiletime %1 "%~dpn1-%~x1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
