@ECHO OFF
@SETLOCAL

IF 'x%1'=='x' (
	net stop Apache2.4
	net start Apache2.4
	SHIFT
) ELSE (
	net %1 Apache2.4
	SHIFT
)

@ENDLOCAL
