"""A Script that tags your movie files.

Run the script in a folder containing the mp4/mkv movie files with their
filename as the movie's title.

This script might seem a little messy and ugly and I know maybe there is
better and effecient way to do some of the tasks.
but I am unaware of them at the moment and am a begginer in Python and
this is my first, or maybe second python script.

TO-DO
1. Add a way to notify when the script is done running
2. Add proper error handleling for ffmpeg
"""
import os
import subprocess
import urllib
import shlex
import linecache
import sys
from json import JSONDecoder
import tmdbsimple as tmdb
from imdbpie import Imdb
from mutagen.mp4 import MP4, MP4Cover


def collect_stream_metadata(filename):
    """
    Returns a list of streams' metadata present in the media file passed as 
    the argument (filename)
    """
    command = 'ffprobe -i "{}" -show_streams -of json'.format(filename)
    args = shlex.split(command)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    
    json_data = JSONDecoder().decode(out)
    
    return json_data
        


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    fname = f.f_code.co_filename
    linecache.checkcache(fname)
    line = linecache.getline(fname, lineno, f.f_globals)
    print ('\nEXCEPTION IN ({}, LINE {} "{}"): {}'.format(fname,
                                                          lineno,
                                                          line.strip(),
                                                          exc_obj))


#  Setting the API key for usage of TMDB API
tmdb.API_KEY = 'b888b64c9155c26ade5659ea4dd60e64'


def collect_files(file_type):
    """
    returns a list of files in the current directory that are of
    the extension passed as string\n
    eg: collect_files('txt') would return a list of all txt files
    """
    filenames = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(file_type):
            filenames.append(filename)
    return filenames


def get_common_files(mediafile_list, srtfile_list):
    """
    returns a list of filenames that are common in mediafile_list and
    strfile_list. \n
    While getting common filenames it ignores the extension.\n
    Also the returned list will have the same file extension the mediafile_list
    files have
    """

    media_filenames = [i[:-4] for i in mediafile_list]
    subtitle_filenames = [i[:-4] for i in srtfile_list]
    media_type = mediafile_list[0][-4:]
    media_set = set(media_filenames)
    srt_set = set(subtitle_filenames)
    common_files = list(media_set & srt_set)
    common_files = [i + media_type for i in common_files]
    common_files.sort()
    return common_files


def remove_common_files(list1, list2):
    """
    returns a subset of list1 that has common elements removed that were found
    in both lists
    or in other words - returns a subset of list1 that has elements unique to
    only list1
    """

    # results in a list of values that are unique to list1
    new_list1 = list(set(list1) - set(list2))
    new_list1.sort()
    return new_list1


def start_process(filenames, mode):
    """
    This is the main funtion of the script
    where it does its main processing.\n
    filenames is the list of files to be processed\n
    mode = 1,2,3 or 4\n
    1 means mp4 to tagged mp4\n
    2 means mp4 with sub to subbed and tagged mp4\n
    3 means mkv to tagged mp4\n
    4 means mkv with sub to subbed and tagged mp4
    """

    for filename in filenames:
        try:
            title = filename[:-4]
            
            stream_md = collect_stream_metadata(filename)
            streams_to_process = []
            dvdsub_exists=False
            for stream in stream_md['streams']:
                if not stream['codec_name'] == "dvdsub":
                    streams_to_process.append(stream['index'])
                else:
                    dvdsub_exists=True
            
            print('\nSearching IMDb for "{}"'.format(title))
            
            imdb = Imdb()
            movie_results = []
            results = imdb.search_for_title(title)
            for result in results:
                if result['type'] == "feature":
                    movie_results.append(result)
                    
            if not movie_results:
                while not movie_results:
                    title = input('\nNo results for "' + title +
                                  '" Enter alternate/correct movie title >> ')
                    
                    results = imdb.search_for_title(title)
                    for result in results:
                        if result['type'] == "feature":
                            movie_results.append(result)
                
            # The most prominent result is the first one
            # mpr - Most Prominent Result
            mpr = movie_results[0]
            print('\nFetching data for {} ({})'.format(mpr['title'],
                                                       mpr['year']))
                                                     
            # imdb_movie is a dict of info about the movie
            imdb_movie = imdb.get_title(mpr['imdb_id'])
            
            imdb_movie_title = imdb_movie['base']['title']
            imdb_movie_year = imdb_movie['base']['year']
            imdb_movie_id = mpr['imdb_id']
                        
            
            imdb_movie_rating = imdb_movie['ratings']['rating']
            
            if not 'outline' in imdb_movie['plot']:
                imdb_movie_plot_outline = (imdb_movie['plot']['summaries'][0]
                                           ['text'])
                print("\nPlot outline does not exist. Fetching plot summary "
                        "instead.\n\n")
            else:
                imdb_movie_plot_outline = imdb_movie['plot']['outline']['text']
            
            # Composing a string to have the rating and the plot of the
            # movie which will go into the 'comment' metadata of the 
            # mp4 file.
            imdb_rating_and_plot = str('IMDb rating ['
                                       + str(float(imdb_movie_rating))
                                       + '/10] - '
                                       + imdb_movie_plot_outline)
                                       
            
            imdb_movie_genres = imdb.get_title_genres(imdb_movie_id)['genres']
            
            # Composing the 'genre' string of the movie.
            # I use ';' as a delimeter to searate the multiple genre values
            genre = ';'.join(imdb_movie_genres)
            
            
            newfilename = (imdb_movie_title
                           + ' ('
                           + str(imdb_movie_year)
                           + ').mp4')
                           
            # We don't want the characters not allowed in a filename
            newfilename = (newfilename
                           .replace(':', ' -')
                           .replace('/', ' ')
                           .replace('?', ''))

            command = ""
            stream_map = []
            for f in streams_to_process:
                stream_map.append("-map 0:{}".format(f))
            stream_map_str = ' '.join(stream_map)           
            
            

            if mode == 1:
                # it is required to rename it as its already an mp4 file that
                # wasn't proccessed by ffmpeg
                os.rename(filename, newfilename)
            if mode == 2 or mode == 4:

                command = ('ffmpeg -i "'
                           + filename
                           + '" -sub_charenc UTF-8 -i "'
                           + filename[:-4]
                           + '.srt" '
                           + stream_map_str
                           + ' -map 1 -c copy -c:s mov_text '
                             '"' + newfilename + '"')
                subprocess.run(shlex.split(command))
            if mode == 3:
                command = ('ffmpeg -i '
                           + '"' + filename + '" '
                           + stream_map_str
                           + ' -c copy -c:s mov_text '
                             '"' + newfilename + '"')
                subprocess.run(shlex.split(command))
                
            if dvdsub_exists:
                print("\nRemoved DVD Subtitles due to uncompatibility with "
                      "mp4 file format")

            # The poster is fetched from tmdb only if there is no file
            # named " filename + '.jpg' " in the working directory
            # this way user can provide their own poster image to be used
            poster_filename = filename[:-4] + '.jpg'
            if not os.path.isfile(poster_filename):
                print('\nFetching the movie poster...')
                tmdb_find = tmdb.Find(imdb_movie_id)
                tmdb_find.info(external_source = 'imdb_id')
                
                path = tmdb_find.movie_results[0]['poster_path']
                complete_path = r'https://image.tmdb.org/t/p/w780' + path
                
                uo = urllib.request.urlopen(complete_path)
                with open(poster_filename, "wb") as poster_file:
                    poster_file.write(uo.read())
                    poster_file.close()
            
            

            video = MP4(newfilename)
            with open(poster_filename, "rb") as f:
                video["covr"] = [MP4Cover(
                                    f.read(),
                                    imageformat=MP4Cover.FORMAT_JPEG)]
                video['\xa9day'] = str(imdb_movie_year)
                video['\xa9nam'] = imdb_movie_title
                video['\xa9cmt'] = imdb_rating_and_plot
                video['\xa9gen'] = genre
                print('\nAdding poster and tagging file...')

            try:
                video.save()
                #  I have encounterd this error in pevious version
                #  of script, now I handle it by removing the metadata
                #  of the file. That seems to solve the probelem
            except OverflowError:
                remove_meta_command = ('ffmpeg -i "' + newfilename
                                       + '" -codec copy -map_metadata -1 "'
                                       + newfilename[:-4] + 'new.mp4"')
                subprocess.run(shlex.split(remove_meta_command))
                video_new = MP4(newfilename[:-4] + 'new.mp4')
                with open(poster_filename, "rb") as f:
                    video_new["covr"] = [MP4Cover(
                                            f.read(),
                                            imageformat=MP4Cover.FORMAT_JPEG)]
                    video_new['\xa9day'] = str(imdb_movie_year)
                    video_new['\xa9nam'] = imdb_movie_title
                    video_new['\xa9cmt'] = imdb_rating_and_plot
                    video_new['\xa9gen'] = genre
                    print('\nAdding poster and tagging file...')

                try:
                    video_new.save()
                    if not os.path.exists('auto fixed files'):
                        os.makedirs('auto fixed files')
                    os.rename(newfilename[:-4]
                              + 'new.mp4', 'auto fixed files\\'
                              + newfilename[:-4] + '.mp4')
                    os.remove(newfilename)

                except OverflowError:
                    errored_files.append(filename
                                         + (' - Could not save even after'
                                            'striping metadata'))
                    continue

            os.remove(poster_filename)
            print('\n' + filename
                       + (' was proccesed successfuly!\n\n===================='
                          '======================================'))
        except Exception as e:
            print('\nSome error occured while processing '
                  + filename
                  + '\n\n====================================================')
            errored_files.append(filename + ' - ' + str(e))
            PrintException()

                                                                               
mp4_filenames = []
mkv_filenames = []
srt_filenames = []
mp4_with_srt_filenames = []
mkv_with_srt_filenames = []
errored_files = []

mp4_filenames = collect_files('mp4')
mkv_filenames = collect_files('mkv')
srt_filenames = collect_files('srt')

# We check whether there are mp4 files and if yes, are there any
# srt files? if yes, then get the mp4 files that have srts associated with them
# then if there are mp4 files that have srt files associated with them then
# remove the others as they are to be proccessed separately
if not len(mp4_filenames) == 0:
    if not len(srt_filenames) == 0:
        mp4_with_srt_filenames = get_common_files(mp4_filenames,
                                                  srt_filenames)
        if not len(mp4_with_srt_filenames) == 0:
            mp4_filenames = remove_common_files(mp4_filenames,
                                                mp4_with_srt_filenames)

if not len(mkv_filenames) == 0:
    if not len(srt_filenames) == 0:
        mkv_with_srt_filenames = get_common_files(mkv_filenames, srt_filenames)
        if not len(mkv_with_srt_filenames) == 0:
            mkv_filenames = remove_common_files(mkv_filenames,
                                                mkv_with_srt_filenames)

# This is where the main process of conversion takes place.
# We simply check the file lists are not empty and then execute the main task
# depending on what type it is according to mode in the funtion "start_process"
if not len(mp4_filenames) == 0:
    start_process(mp4_filenames, 1)

if not len(mp4_with_srt_filenames) == 0:
    start_process(mp4_with_srt_filenames, 2)

if not len(mkv_filenames) == 0:
    start_process(mkv_filenames, 3)

if not len(mkv_with_srt_filenames) == 0:
    start_process(mkv_with_srt_filenames, 4)

if (len(mp4_filenames) == 0 and len(mkv_filenames) == 0
        and len(mp4_with_srt_filenames) == 0
        and len(mkv_with_srt_filenames) == 0):
    print('There were no MP4 or MKV files found in the directory')
else:
    # Checks if there were any files that caused the Overflow Error,
    # if yes then prints them out.
    if len(errored_files) == 0:
        print('\n\n\nAll files proccessed successfuly!')
    else:
        print('\n\n\nThe files that were not proccessed: \n')
        for er in errored_files:
            print(er)
