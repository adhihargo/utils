# Utilities

Things I hack together on _mager_ weekends. 

## ffmpeg_2mp3

Something to convert video file to an MP3 audio file. It uses `ffprobe` on source file to determine appropriate audio bitrate.

## ffmpeg_strip_audio/video

At times, you don't need the noise or just the noise (for further processing).

Usage: `ffmpeg_strip_audio FILE`

With input `a.mp4`, output of `strip_audio` is `a-.mp4` and for `strip_video` is `a_audio.mp4`.

## ffmpeg_join_av

Losslessly rejoin audio and video files. I loathe watching videos with ridiculously low audio volume, so I extract the audio to process in a DAW, then join it back with this script. Why such convoluted workflow? Saves me hours of recompressing, that's why.

Usage: `ffmpeg_join_av FILE`

The assumptions are that `FILE` is an MP4 video file, and a corresponding `FILE_audio.m4a` to join it with exists.

Example:
- `ffmpeg_join_av a.mp4` joins `a.mp4` with `a_audio.mp4` (if exist) into `a_av.mp4`.

## ffmpeg_cut

Losslessly cut an audio or video file.

Usage: `ffmpeg_cut.py [-h] [-s START] [-e END] [-y] [-V] [--suffix SUFFIX] FILE` 

Arguments:
- `-s START`: Timestamp of starting point to cut from.
- `-e END`: Timestamp of end point to cut to.
- `--suffix SUFFIX`: Suffix to be appended to resulting filename.
- `-y`: Suppress question if file exists.
- `-V`: Verbosity

## lnlatest

Instead of using installers, I prefer to extract zipped versions of programs I use, then symlink them to a generic name (e.g. `E:\blender-2.79b-windows64` to `E:\blender`). Shortcuts can then just refer to the symlink and remain unchanged, even if the symlink points to a newer version. This script creates a link to the latest subdirectory in a path with names matching a pattern. Wrote it because I'm sick of constantly removing old symlink to create a different one targeting newer (manually typed) directory path.

Usage: `lnlatest.py [-h] [-d DIR_PATH] [-e] LINK PATTERN`

Arguments:
- `-d DIR_PATH`: Specify root directory. If unspecified, it defaults to current working directory.
- `-e`: Automatically remove old symlink. Both `mklink` and `ln` won't overwrite existing link, so usually this is what we'd want. Putting it anyway just to make sure.
- `LINK`: Symlink name to be created.
- `PATTERN`: Glob pattern of directories to be matched. For example, `emacs-*` matches `emacs-26.1-x86_64`, `emacs-25.0-x86_64`, etc. Latest matching directory will be targeted if found.

## wmctrl_gridmove

When I use Gnome DE, I miss [JGPaiva's GridMove](http://www.dcmembers.com/jgpaiva/). So I wrote this script, a crude approximation of GridMove's template I use most using `wmctrl` and X utils. It's meant to be called through custom keyboard shortcut.

Usage: `wmctrl_gridmove.py [-h] [-d DISPLAY_ID] {l,r,m}`

Arguments:
- `-d DISPLAY_ID`: Move active window to assigned monitor, 0-indexed.
- `POS`: Positional argument, either `l`, `r` or `m` to move and resize active window to the left or right side or maximized, respectively, of assigned monitor.

Example:
- `wmctrl_gridmove.py -m 0 l` moves active window to 1st monitor's left side. Simple, eh?