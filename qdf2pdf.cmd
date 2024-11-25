@ECHO OFF
@SETLOCAL

:loop
IF NOT 'x%1'=='x' (
	fix-qdf "%~dpn1.qdf" > "%~dpn1.fdf"
	qpdf "%~dpn1.fdf" "%~dpn1~.pdf"
	nircmd clonefiletime "%~dpn1.qdf" "%~dpn1~.pdf"
	del "%~dpn1.fdf"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
