@ECHO OFF
@SETLOCAL

ffmpeg -i "%~1" -vcodec copy -af "volume=%2" "%~n1_amp%~x1"
nircmd clonefiletime %1 "%~n1_amp%~x1"

@ENDLOCAL
