@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF 'x%1'=='x' (
	ECHO Drag a video file [.mp4] and cover image file [.jpeg, .jpg] to this script.
	GOTO :help_envvar
	GOTO :exit
)

IF 'x%PATH_PODCAST%'=='x' (
	:help_envvar
	ECHO Environment variable PATH_PODCAST must be defined.
	PAUSE
	GOTO :exit
)

:loop
IF NOT 'x%1'=='x' (
	IF '%~x1'=='.jpg' (
		SET COVER="%~1"
		ECHO COVER: !COVER!
	) ELSE IF '%~x1'=='.jpeg' (
		SET COVER="%~1"
		ECHO COVER: !COVER!
	) ELSE IF '%~x1'=='.mp4' (
		SET VIDEO="%~1"
		ECHO VIDEO: !VIDEO!
	) ELSE IF '%~x1'=='.m4a' (
		SET VIDEO="%~1"
		ECHO VIDEO: !VIDEO!
	)

	IF NOT 'x!COVER!'=='x' IF NOT 'x!VIDEO!'=='x' (
		FOR %%I IN (!VIDEO!) DO (
			SET VIDEO_DIR=%%~dpI
			SET VIDEO_BASE=%%~nI
		)
		move !COVER! "!VIDEO_DIR!\cover.jpeg"
		ren !VIDEO! "!VIDEO_BASE!.aac"
		CALL ffmpeg_setcover.cmd "!VIDEO_DIR!\!VIDEO_BASE!.aac"
		move "!VIDEO_DIR!\!VIDEO_BASE!.m4a" %PATH_PODCAST%

		REM Cleanup for next iteration
		SET COVER=
		SET VIDEO=
	)
	SHIFT /1

	GOTO :loop
)

:file_index
py -3 "%~dp0\file_index_latest.py" %PATH_PODCAST% -e m4a -a

:exit

ENDLOCAL
rem Local Variables:
rem tab-width: 4
rem End:
