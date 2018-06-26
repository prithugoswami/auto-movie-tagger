# Auto Movie Tagger
A Python script that auto tags and adds poster to MKV or MP4 movie files.  
Also adds subtitles if provided.  

The metadata it adds:
+ Genre - Movie's genres
+ Year - The release year of the movie
+ Comment - IMDb Rating and the movie's plot-outline.

![first](https://user-images.githubusercontent.com/28246690/34607517-11481cd8-f23a-11e7-93de-0231b36dee7e.png)

## Requirements

  <ul>
    <li>python 3.x</li>
    <li><a href="https://ffmpeg.org/">ffmpeg</a> - A cli-tool that can encode/decode media files</li>
    <li><a href="https://pypi.python.org/pypi/imdbpie">imdbpie</a> - A Python module for IMDb</li>
    <li><a href="https://pypi.python.org/pypi/tmdbsimple">tmdbsimple</a> - A Python module which is a wrapper for The Movie Database API v3</li>
    <li><a href="https://pypi.python.org/pypi/mutagen">mutagen</a> - Python module to handle media files' metadata</li>
  </ul>

><h3>Note for Linux Users with both python2 and python3 installed on their system</h3>
>This script is compatible for python3 only. If you are on Ubuntu with python2.x and python3.x both installed, install pip3 using</p>
><pre>sudo apt-get install pip3</pre>
>and then install the dependencies:
><pre>pip3 install &lt;module&gt;</pre>




## Installing ffmpeg
You need to first download ffmpeg (<a href="https://ffmpeg.org/download.html">from here</a>) and add it to your PATH variable.  
Here's a <a href="http://www.wikihow.com/Install-FFmpeg-on-Windows">wikiHow article on how to install ffmpeg on Windows</a>

## Installing Python module dependencies
<pre>pip install imdbpie tmdbsimple mutagen</pre>

## How to use
<ol>
  <li>Move all the movie files you want to be tagged into one folder. Make sure that the filename is the correct title of the movie. Year of the title can also be included.</li>
  <li>If you want subtitles to be embedded into the movie file(s) then add a subtitle file (.srt only) in the same folder named exactly the same as the movie file(s).</li>
  <li>Download the script (<a href="amt.py">amt.py</a>) and run it in that directory and sit back and relax till it ends executing. How to run the script in that directory? Copy the script in the directory and run it using the command:
  <pre><code>python amt.py</code></pre>
  Ubuntu users with python2.x and python3.x both installed, make sure the depedences are installed using <code>pip3 install &lt;module&gt;</code> and then run the script using:  
  <pre>python3 amt.py</pre>
  </li>
</ol>

## Notes
<ul>
  <li>This script only works for mp4 and mkv file types.</li>
  <li>The final file is always a MP4 file.</li>
  <li>Make sure if you are having a MKV file, it should not contain picture based subtitles (hdmv-pgs/vobsub,etc) as MP4 files do not support picture based subtitles. You can use <a href="https://mkvtoolnix.download/">MKVToolNix</a> or any other similar GUI utility to quickly remove the picture based subtitles or you can use ffmpeg to this as well. If the file already has an SRT subtitle then the script will just copy it.</li>
  <li>If you would like to use your own poster image then add an image file (jpg only) in the same folder and rename it to the same name as the movie file.</li>
  <li>Although I have provided my own TMDb API key in the source, I would recommend you get you own from <a href="https://www.themoviedb.org/documentation/api">here</a></li>
  <li> Tip - When you sort your tagged movies according to the comment they get sorted by ascending/descending order of their IMDb rating.</li>
</ul>

## Tooltips for Windows Users
![tooltip](https://user-images.githubusercontent.com/28246690/34607523-1e526a14-f23a-11e7-8f49-74c4c0a8454c.png)

To make the tooltip show the movie's genre and IMDb rating and plot-outline like in the screenshot, you will have to make some changes in the registry of your windows machine.
1. Fire up your _Registry Editor_. Open the _Run_ window (Win + R) and type "regedit"
2. Head over to <strong>HKEY_CLASSES_ROOT\SystemFileAssociations\\.mp4</strong>
3. From the left panel right click on the "<strong>InfoTip</strong>" value name and click "<strong>Modify...</strong>"
4. Under the "<strong>Value Data</strong>" field add the attributes, "System.Music.Genre" and "System.Comment" anywhere you like depending how you would like the metadata to show in the tool tip. The "<strong>Value Data</strong>" filed consists of different attributes that appear in the tooltip. For example "System.Media.Duration" is the Duration of the media. These attributes are separated by ";" (semicolon). I would recommend adding the Genre and Comment attributes after "System.Media.Duration".
