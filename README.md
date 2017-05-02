# Auto Movie Tagger
A Python script that auto tags and adds poster to mkv or mp4 movie files.  

The metadata it adds:
+ Genre - Movie's genres
+ Artist - The director of the movie
+ Year - The release year of the movie
+ Comment - IMDb Rating and the movie's plot-outline.

![The Matrix](/promo-images/matrix.png)
![Wall-E](/promo-images/walle.png)
![Doctor Strange](/promo-images/strange.png) 

## Requirements
<ul>
  <li><a href="https://ffmpeg.org/">ffmepeg</a> - A cli-tool that can encode/decode media files</li>
  <li><a href="https://pypi.python.org/pypi/imdbpie">imdbpie</a> - A Python module for IMDb</li>
  <li><a href="https://pypi.python.org/pypi/tmdbsimple">tmdbsimple</a> - A Python wrapper for The Movie Database API v3</li>
  <li><a href="https://pypi.python.org/pypi/mutagen">mutagen</a> - Python module to handle media files' metadata</li>
</ul>

## Installing ffmpeg
You need to first download ffmpeg <a href="https://ffmpeg.org/download.html">(from here)</a> and add it to your PATH variable if on windows.  
Here's a <a href="http://www.wikihow.com/Install-FFmpeg-on-Windows">wikiHow article on how to install ffmpeg on Windows</a>

## Installing Python module dependencies
<ul>
  <li>imdbpie  <pre><code>pip install imdbpie</code></pre></li>
  <li>tmdbpie  <pre><code>pip install tmdbsimple</code></pre></li>
  <li>mutagen  <pre><code>pip install mutagen</code></pre></li>
</ul>

## How to use
<ol>
  <li>Move all the movie files you want to be tagged into one folder</li>
  <li>If you want subtitles to be embeded into the movie file(s) then add a subtitle file (srt only) in the same folder named exactly the same as the movie file(s).</li>
  <li>Run the script in that directory and sit back and relax till it ends executing. </li>
</ol>

## Notes
<ul>
  <li>This script only works for mp4 and mkv file types.</li>
  <li>The final file is a mp4 file</li>
  <li>Make sure if you are having an mkv file, it should not contain any type of picture based subtitles(hdmv-pgs/vobsub,etc). You can use <a href="https://mkvtoolnix.download/">MKVToolNix</a> or any other similar gui utility to quickly remove the picture based subtitles or you can use ffmpeg to this as well. If the file already has an srt subtitle then the script will just copy it.</li>
  <li>If you would like to use your own poster image then add an image file (jpg only) in the same folder and rename it to the same as the movie file.</li>
  <li>Although I have provided my own TMDb API key in the source, I would recommend you get you own from <a href="https://www.themoviedb.org/documentation/api">here</a></li>
  <li> Tip - When you sort your tagged movies according to the comment they get sorted by ascending/descending order of their IMDb rating.</li>
</ul>

