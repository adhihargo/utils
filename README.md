# Utilities

Things I hack together on _mager_ weekends.

## ffmpeg_2mp3

Something to convert video file to an MP3 audio file. It uses `ffprobe` on source file to determine appropriate audio bitrate.

## ffmpeg_2mp4

Blindly convert to MP4, any files that can logically be converted to MP4 using `ffmpeg`. 

## ffmpeg_strip_audio/video

At times, you don't need the noise or just the noise (for further processing).

### Usage: 
`ffmpeg_strip_audio FILE`

With input `a.mp4`, output of `strip_audio` is `a-.mp4` and for `strip_video` is `a_audio.mp4`.

## ffmpeg_amplify

Amplify audio by explicit value or automatically based on original file's max loudness. If amplification level is determined based on original file's loudness, file will not be processed if it's outside `MIN_THRESHOLD` and `MAX_THRESHOLD` (see Arguments).

### Usage: 
`    ffmpeg_amplify.py [-h] [-v VOLUME] [-s] [-m MIN_THRESHOLD]
    [-M MAX_THRESHOLD] [-y] [-V] [--suffix SUFFIX]
    FILE`

### Arguments:
- `-v  VOLUME`, `--volume VOLUME`: Manually set volume amplification level.
- `-s`, `--show_only`: Show `FILE`'s current volume level, then exit.
- `-m MIN_THRESHOLD`, `--min_threshold MIN_THRESHOLD`: (Abs. value, default: 1.0)
- `-M MAX_THRESHOLD`, `--max_threshold MAX_THRESHOLD`: (Abs. value, default: 30.0)
- `--suffix SUFFIX`: Suffix to be appended to resulting filename.
- `-y`: Suppress question if file exists.
- `-V`: Verbosity

## ffmpeg_join_av

Losslessly rejoin audio and video files. I loathe watching videos with ridiculously low audio volume, so I extract the audio to process in a DAW, then join it back with this script. Why such convoluted workflow? Saves me hours of recompressing, that's why.

### Usage: 
`ffmpeg_join_av FILE`

The assumptions are that `FILE` is an MP4 video file, and a corresponding `FILE_audio.m4a` to join it with exists.

Example:
- `ffmpeg_join_av a.mp4` joins `a.mp4` with `a_audio.mp4` (if exist) into `a_av.mp4`.

## ffmpeg_cut

Losslessly cut an audio or video file.

### Usage: 
`ffmpeg_cut.py [-h] [-s START] [-e END] [-y] [-V] [--suffix SUFFIX] FILE` 

### Arguments:
- `-s START`: Timestamp of starting point to cut from.
- `-e END`: Timestamp of end point to cut to.
- `--suffix SUFFIX`: Suffix to be appended to resulting filename.
- `-c`: Mark input `FILE` as config file. If set, other switches but `-y` and `-V` are ignored.
- `-y`: Suppress question if file exists.
- `-V`: Verbosity

If `-c` is set, script assumes `FILE` to be a configuration file with the following format:

<pre>
[main]
src=FILE.mp4  # path to file
sections=1 2 3  # space separated sections to process

[sections]
1=
2=01:01  # starting timestamp for a section, first one left empty  
3=02:02
9=03:03  # to write any but the last section, put any number 
</pre>

## lnlatest

Instead of using installers, I prefer to extract zipped versions of programs I use, then symlink them to a generic name (e.g. `E:\blender-2.79b-windows64` to `E:\blender`). Shortcuts can then just refer to the symlink and remain unchanged, even if the symlink points to a newer version. This script creates a link to the latest subdirectory in a path with names matching a pattern. Wrote it because I'm sick of constantly removing old symlink to create a different one targeting newer (manually typed) directory path.

### Usage: 
`lnlatest.py [-h] [-d DIR_PATH] [-e] LINK PATTERN`

Arguments:
- `-d DIR_PATH`: Specify root directory. If unspecified, it defaults to current working directory.
- `-e`: Automatically remove old symlink. Both `mklink` and `ln` won't overwrite existing link, so usually this is what we'd want. Putting it anyway just to make sure.
- `LINK`: Symlink name to be created.
- `PATTERN`: Glob pattern of directories to be matched. For example, `emacs-*` matches `emacs-26.1-x86_64`, `emacs-25.0-x86_64`, etc. Latest matching directory will be targeted if found.

## create_prog_batch / create_prog_shortcut

For each file passed as arguments, create shortcut either as batch script or Windows link. `create_prog_shortcut` depends on `create-shortcut.exe` included in [Git for Windows](https://github.com/git-for-windows/git) distribution. 

### Usage:

* `create_prog_batch FILE+`
* `create_prog_shortcut FILE+`

These will place a shortcut to each `FILE`s in the path stored in `PROG_PATH` environment variable (defaults to `C:\prog`).

## pdf2qdf, qdf2pdf

Converts PDF to and from QDF, using [qpdf](https://github.com/qpdf/qpdf). I use these to edit a PDF file's page numbering.

### Usage:
`pdf2qdf|qdf2pdf PDF_FILE`

Input for `qdf2pdf` is also the PDF file, just so I can do the fewest change to the original command when converting back to PDF.

## pdfdata

Dump and update PDF metadata, using [PDFtk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/). I use this to edit a PDF file's bookmark list (table of contents).

### Usage:
`pdfdata.py [-h] [-d [DATAFILE]] [-s [DATAFILE]] [-T [TOCFILE]]
                  [-t [TOCFILE]] [-o [OUTPUT]]
                  FILE`

- `-d [DATAFILE]`, `--dump [DATAFILE]`: Dump PDF data to file.
- `-s [DATAFILE]`, `--set [DATAFILE]`: Set PDF data from file.
- `-T [TOCFILE]`, `--dump_toc [TOCFILE]`: Dump PDF bookmark data to a TOC file.
- `-t [TOCFILE]`, `--toc [TOCFILE]`: Set PDF bookmark data from TOC file.
- `-o [OUTPUT]`, `--output [OUTPUT]`: Output PDF file if setting PDF data.

## act / deact

Just a pair of scripts to save keystrokes, to activate/deactivate Python virtual environment.

### Usage:

* `act C:\prog\venv\37_app` is akin to calling that venv's `activate.bat`.
* `deact` exists just to save 5+ keystrokes to call `deactivate.bat`.

## pkill

Kill a process by its executable basename.

## wmctrl_gridmove

When I use Gnome DE, I miss [JGPaiva's GridMove](http://www.dcmembers.com/jgpaiva/). So I wrote this script, a crude approximation of GridMove's template I use most using `wmctrl` and X utils. It's meant to be called through custom keyboard shortcut.

### Usage: 
`wmctrl_gridmove.py [-h] [-d DISPLAY_ID] {l,r,m}`

### Arguments:
- `-d DISPLAY_ID`: Move active window to assigned monitor, 0-indexed.
- `POS`: Positional argument, either `l`, `r` or `m` to move and resize active window to the left or right side or maximized, respectively, of assigned monitor.

Example:
- `wmctrl_gridmove.py -m 0 l` moves active window to 1st monitor's left side. Simple, eh?
