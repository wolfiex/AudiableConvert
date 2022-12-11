'''
Conversion functions for Audiable Convert

must remove conda ffprobe 
rm /Users/user/opt/miniconda3/bin/ffprobe
'''

import os, json, time, sys
from p_tqdm import p_map

# convert seconds into timecode
hhmmss = lambda x: time.strftime('%H:%M:%S', time.gmtime(float(x)))

def get_chapters(file):
    ''' 
    A function to get the relevant chapters for Audiable
    '''

    # read the chapters
    chapters = json.loads(os.popen(f'ffprobe -i {file} -print_format json -show_chapters -loglevel error').read())['chapters']

    return chapters



def convert(file,key,out=os.getcwd()):
    
    name = os.path.basename(file).split('.')[0].replace('_ep5','')
    if out[-1] != '/': out += '/'
    outfile = out+name+'/'

    try:
        os.mkdir(outfile)
    except:
        print( name,' already exists\n --- SKIPPING ---')
        return None

    # read the chapters
    chapters = json.loads(os.popen(f'ffprobe -i {file} -print_format json -show_chapters -loglevel error').read())['chapters']

    def writechapter(ch):
        cid = ch["id"]
        try:cid = '%03d'%cid
        except:...

        os.popen(f'ffmpeg -activation_bytes {key} -ss {hhmmss(ch["start_time"])} -to {hhmmss(ch["end_time"])} -i {file} -metadata title="{ch["tags"]["title"]}" -codec copy {outfile}ch{cid}_{name}.m4b -y -loglevel quiet -stats')

    p_map(writechapter, chapters)

    print('Finished converting ' + name)