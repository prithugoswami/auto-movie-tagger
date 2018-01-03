"""A Script that tags you movie files.

Run the script in a folder containing the mp4/mkv movie files with their
filename as the movie's title.

This script might seem a little messy and ugly and I know maybe there is
better and effecient way to do some of the tasks.
but I am unaware of them at the moment and am a begginer in Python and
this is my first, or maybe second python script.

TO-DO
1. Add a way to notify when the script is done running
2. Seems a little too much for now but I could change/add stream specific
metadata according to the file
For example depending upon what kind of audio the mkv file has (like AAC 5.1,
DTS 5.1), the script can also change the title/handler of the audio stream
right now it just blanks it out.
The same can be done for subtitles depending upon language. This can also be
implemented to discard dvd subtitles that are sometimes found
in MKVs but are not supported by MP4
3. Add proper error handleling for ffmpeg
"""
import os
import subprocess
import urllib
import shlex
import linecache
import sys
import tmdbsimple as tmdb
from imdbpie import Imdb
from mutagen.mp4 import MP4, MP4Cover


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    fname = f.f_code.co_filename
    linecache.checkcache(fname)
    line = linecache.getline(fname, lineno, f.f_globals)
    print ('\nEXCEPTION IN ({}, LINE {} "{}"): {}'.format(fname, lineno, line.strip(), exc_obj))


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

    searchindex = 0
    for filename in filenames:
        try:
            title = filename[:-4]

            print('\nFetching movie data for "' + title + '"')
            search = tmdb.Search()
            srch_response = search.movie(query=title)
            # getting a Movies object from the id that we got from the search
            # results
            try:    # sometimes blank search results are returned
                tmdb_movie = tmdb.Movies(srch_response['results'][searchindex]['id'])
            except IndexError:
                while len(srch_response['results']) == 0:
                    title = input("\nCould not find the movie, Enter"
                                  " alternate movie title >> ")

                    searchindex = int(input('Search result index >> '))
                    response = search.movie(query=title)
                    try:
                        tmdb_movie = (tmdb.Movies(response['results']
                                      [searchindex]['id']))
                    except IndexError:
                        continue
            # we get the info about the movie
            movie_response = tmdb_movie.info()
            # making an imdb object
            imdb = Imdb()
            # tmdb_movie.imdb_id is the imdb id of the moovie that we searched
            # before usng tmdb
            imdb_movie = imdb.get_title_by_id(tmdb_movie.imdb_id)
            # using imdb provided movie name and
            newfilename = (imdb_movie.title
                           + ' ('
                           + str(imdb_movie.year)
                           + ').mp4')
            newfilename = (newfilename
                           .replace(':', ' -')
                           .replace('/', ' ')
                           .replace('?', ''))

            command = ""

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
                           + '-map 0 -map 1 -c copy -c:s mov_text '
                             '-metadata:s:s:0 handler="English Subtitle" '
                             '-metadata:s:s:0 language=eng '
                             '-metadata:s:a:0 handler="" '
                             '-metadata:s:v:0 handler="" "'
                             + newfilename + '"')
                subprocess.run(shlex.split(command))
            if mode == 3:
                command = ('ffmpeg -i "'
                           + filename
                           + '" -c copy -c:s mov_text '
                             '-metadata:s:s:0 handler="English" '
                             '-metadata:s:s:0 language=eng '
                             '-metadata:s:a:0 handler="" '
                             '-metadata:s:v:0 handler="" '
                             '"' + newfilename + '"')
                subprocess.run(shlex.split(command))

            # the poster is fetched from tmdb only if there is no file
            # named " filename + '.jpg' " in the working directory
            # this way user can provide their own poster image to be used
            poster_filename = filename[:-4] + '.jpg'
            if not os.path.isfile(poster_filename):
                print('\nFetching the movie poster...')
                path = srch_response['results'][searchindex]['poster_path']
                poster_path = r'https://image.tmdb.org/t/p/w640' + path

                uo = urllib.request.urlopen(poster_path)
                with open(poster_filename, "wb") as poster_file:
                    poster_file.write(uo.read())
                    poster_file.close()

            imdb_rating_and_plot = str('IMDb rating ['
                                       + str(float(imdb_movie.rating))
                                       + '/10] - '
                                       + imdb_movie.plot_outline)
            # setting the genres of the movie. I use ';' as a delimeter
            # to searate the multiple genre values
            genre = ';'.join(imdb_movie.genres)
            # Going overboard and adding directors name to artist tag of
            # the mp4 file
            directors = imdb_movie.directors_summary
            director = directors[0].name

            video = MP4(newfilename)
            with open(poster_filename, "rb") as f:
                video["covr"] = [MP4Cover(
                                    f.read(),
                                    imageformat=MP4Cover.FORMAT_JPEG)]
                video['\xa9day'] = str(imdb_movie.year)
                video['\xa9nam'] = imdb_movie.title
                video['\xa9cmt'] = imdb_rating_and_plot
                video['\xa9gen'] = genre
                video['\xa9ART'] = director
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
                    video_new['\xa9day'] = str(imdb_movie.year)
                    video_new['\xa9nam'] = imdb_movie.title
                    video_new['\xa9cmt'] = imdb_rating_and_plot
                    video_new['\xa9gen'] = genre
                    video_new['\xa9ART'] = director
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
