@ECHO OFF
@SETLOCAL

ffmpeg -i %1 -map 0:1 -codec copy "%~n1_audio%~x1"
nircmd clonefiletime %1 "%~n1_audio%~x1"

@ENDLOCAL
