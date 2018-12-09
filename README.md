# Utilities

Things I hack together on _mager_ weekends. 

## 2mp3

Something to convert video file to an MP3 audio file. It uses `ffprobe` on source file to determine appropriate audio bitrate. 

## wmctrl_gridmove

When I use Gnome DE, I miss [JGPaiva's GridMove](http://www.dcmembers.com/jgpaiva/). So I wrote this script, a crude approximation of GridMove's template I use most using `wmctrl` and X utils. It's meant to be called through custom keyboard shortcut.

Arguments:
- `-d DISPLAY_INDEX`: Move active window to assigned monitor, 0-indexed.
- `POS`: Positional argument, either `l` or `r` to move and resize active window to the left or right side, respectively, of assigned monitor.

Example:
- `wmctrl_gridmove.py -m 0 l` moves active window to 1st monitor's left side. Simple, eh?