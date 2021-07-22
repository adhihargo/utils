@ECHO OFF
@SETLOCAL EnableDelayedExpansion

rem For a file a.mp4, look for existence of a_audio.m4a (output of ffmpeg_strip_video
rem processed by Audacity) then join the original's video channel with _audio.m4a's
rem audio.
SET AUDIO="%~n1_audio.m4a"
SET TARGET="%~n1_av%~x1"
IF NOT EXIST %AUDIO% (
	GOTO QUIT
)
ECHO Ada %AUDIO%

ffmpeg -i "%~1" -i %AUDIO% -map 0:v:0 -map 1:a:0 -codec copy %TARGET%
nircmd clonefiletime "%~1" %TARGET%

:QUIT
@ENDLOCAL
