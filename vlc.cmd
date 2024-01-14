@ECHO OFF
@SETLOCAL

START %VLCPATH%\vlc.exe --no-playlist-autostart %*

@ENDLOCAL
