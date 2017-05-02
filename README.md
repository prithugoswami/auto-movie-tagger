# Auto Movie Tagger
A Python script that auto tags and adds poster to mkv or mp4 movie files. 

![The Matrix](/promo-images/matrix.png)
![Wall-E](/promo-images/walle.png)
![Doctor Strange](/promo-images/strange.png) 

## Requirements
<ul>
  <p><a href="https://ffmpeg.org/">ffmepeg</a> - A cli-tool that can encode/decode media files</p>
  <p><a href="https://pypi.python.org/pypi/imdbpie">imdbpie</a> - A Python module for IMDb</p>
  <p><a href="https://pypi.python.org/pypi/tmdbsimple">tmdbsimple</a> - A Python wrapper for The Movie Database API v3</p>
  <p><a href="https://pypi.python.org/pypi/mutagen">mutagen</a> - Python module to handle media files' metadata
</ul>

## Installing ffmpeg
You need to first download ffmpeg ((from here))[https://ffmpeg.org/download.html] and add it to your PATH variable if on windows.  
Here's a (wikiHow article on how to install ffmpeg on Windows)[http://www.wikihow.com/Install-FFmpeg-on-Windows]

## Installing Python module dependencies
<ul>
  <p>imdbpie - <pre><code>pip install imdbpie</code></pre></p>
  <p>tmdbpie - <pre><code>pip install tmdbsimple</code></pre></p>
  <p>mutagen - <pre><code>pip install mutagen</code></pre></p>
</ul>

## How to use
<ol>
  <p>Move all the movie files you want to be tagged into one folder</p>
  <p>If you want subtitles to be embeded into the movie file(s) then add a subtitle file (srt only) in the same folder named exactly the same as the movie file(s).</p>
  <p>Run the script in that directory and sit back and relax till it ends executing.</p>
</ol>

## Notes
<ul>
  <p>This script only works for mp4 and mkv file types.</p>
  <p>Make sure if you are having an mkv file, it should not contain any type of picture based subtitles(hdmv-pgs/vobsub,etc). You can use (MKVToolNix)[https://mkvtoolnix.download/] or any other similar gui utility to quickly remove the picture based subtitles. If the file already has an srt subtitle then the script will just copy it.</p>
  <p>If you would like to use your own poster image then add an image file (jpg only) in the same folder and rename it to the same as the movie file.</p>
  <p>Although I have provided my own TMDb API key in the source, I would recommend you get you own from (here)[https://www.themoviedb.org/documentation/api]
</ul>

