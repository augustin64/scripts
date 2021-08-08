from ShazamAPI import Shazam
import time, os

for file in os.listdir('./musics'):

    extension = file.split('.')[-1]
    number = file.split(' ')[0]

    file_content_to_recognize = open('./musics/'+file, 'rb').read()

    shazam = Shazam(file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    time.sleep(4)

    song_data = next(recognize_generator)[1]
    try :
        song_name = song_data['track']['title']
        os.rename('./musics/'+file, str('./musics/'+number +' - '+song_name + '.' + extension))
    except :
        print(song_name)
