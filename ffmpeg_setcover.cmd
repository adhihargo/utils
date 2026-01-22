@ECHO OFF
@SETLOCAL

:loopstart
IF NOT 'x%1'=='x' (
IF NOT '%~x1'=='.aac' GOTO :get
	ffmpeg -hide_banner -i "%~1" -i "%~dp1\cover.jpeg" -map 0:a:0 -map 1 -frames:v 1 -disposition:1 attached_pic -codec copy "%~dpn1.m4a"
	nircmd clonefiletime %1 "%~dpn1.m4a"
	del "%~1"
	goto :loopend
:get
	ffmpeg -hide_banner -y -i "%~1" -map 0:v:0 -c:v mjpeg -frames:v 1 "%~dp1\cover.jpeg"
	rem @del "%~1"
:loopend
	SHIFT
	GOTO :loopstart
)
GOTO :exit

:exit
@ENDLOCAL
