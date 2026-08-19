@ECHO OFF
SETLOCAL

SET GS_BIN=mgs
SET GS_ARGS=-sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH

:loop
IF NOT 'x%1'=='x' (
	%GS_BIN% %GS_ARGS% -sOutputFile="%~dpn1~%~x1" "%~1"
	SHIFT
	GOTO loop
)

ENDLOCAL
