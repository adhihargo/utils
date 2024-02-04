@ECHO OFF
@SETLOCAL

ffmpeg -i "%~1" -af "volumedetect" -vn -sn -dn -f null NUL 2> _
type _ | grep max_volume | awk '{print $5}'
del _

@ENDLOCAL
