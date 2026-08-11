@ECHO OFF
@SETLOCAL

IF NOT 'x%1'=='x' (
	SET VLC_PORT=%1
) ELSE (
	SET VLC_PORT=4212
)
ECHO %VLC_PORT%

START %PATH_VLC%\vlc --extraintf rc --rc-quiet --rc-host=127.0.0.1:%VLC_PORT%

@ENDLOCAL
