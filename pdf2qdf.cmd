@ECHO OFF
@SETLOCAL

qpdf -qdf "%~1" "%~n1.qdf"

@ENDLOCAL
