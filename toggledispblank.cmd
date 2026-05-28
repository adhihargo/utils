@REM Created with create_prog_batch 
@ECHO OFF
SETLOCAL

REM To change which display to toggle blank, write display name into
REM textfile [SCRIPTNAME].txt in the same directory as this
REM script. Otherwise it defaults to the first display.
FOR /F "tokens=*" %%i IN (%~dp0\%~n0.txt) DO SET MULTISCREEN_DISPLAY=%%i
IF 'x%MULTISCREEN_DISPLAY%'=='x' (
	SET MULTISCREEN_DISPLAY=\\.\DISPLAY1
)

start %PATH_MULTISCREENBLANK%\MultiscreenBlank2.exe /toggle id %MULTISCREEN_DISPLAY%

ENDLOCAL
