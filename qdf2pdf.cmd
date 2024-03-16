@ECHO OFF
@SETLOCAL

fix-qdf "%~n1.qdf" > "%~n1.fdf"
qpdf "%~n1.fdf" "%~n1~.pdf"
del "%~n1.fdf"

@ENDLOCAL
