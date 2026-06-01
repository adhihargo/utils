@ECHO OFF
@SETLOCAL

:loopstart
IF NOT 'x%1'=='x' (
IF '%~x1'=='.webp' GOTO :convertcover
IF '%~x1'=='.mp4' GOTO :getcover
	ffmpeg -hide_banner -i "%~1" -i "%~dp1\cover.jpeg" -map 0:a:0 -map 1 -frames:v 1 -disposition:1 attached_pic -codec copy "%~dpn1.m4a"
	nircmd clonefiletime %1 "%~dpn1.m4a"
	del "%~1"
	GOTO :loopend
:convertcover
	magick -quality 85 "%~1" "%~dp1\cover.jpeg"
	IF ERRORLEVEL 1 GOTO :loopend
	del "%~1"
	GOTO :loopend
:getcover
	ffmpeg -hide_banner -y -i "%~1" -map 0:v:0 -c:v mjpeg -frames:v 1 "%~dp1\cover.jpeg"
:loopend
	SHIFT
	GOTO :loopstart
)
GOTO :exit

:exit
@ENDLOCAL
