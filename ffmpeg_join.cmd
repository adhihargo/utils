@ECHO OFF
@SETLOCAL

REM For any text file FN.txt provided, join filenames listed "file
REM 'input.mp4'" (-safe 0 = relative path) into FN.mp4. MPEG-4
REM assumed.
:loop
IF NOT 'x%1'=='x' (
	ffmpeg -hide_banner -f concat -safe 0 -i "%~1" -codec copy "%~dpn1"
	SHIFT
	GOTO :loop
)

@ENDLOCAL
