@ECHO OFF
@SETLOCAL

ffmpeg -i "%~1" -map 0:0 -codec copy "%~n1-%~x1"
nircmd clonefiletime %1 "%~n1-%~x1"

@ENDLOCAL
