@ECHO OFF
@SETLOCAL

IF 'x%1'=='x' (
	GOTO :exit
) ELSE (
	SET SRCFILEPATH="%~1"
)

:loop
IF NOT 'x%2'=='x' (
	ECHO Copying file time to "%~nx2"
	nircmdc clonefiletime %SRCFILEPATH% "%~2"
	SHIFT
	GOTO :loop
)

:exit

@ENDLOCAL

rem Local Variables:
rem tab-width: 4
rem End:
