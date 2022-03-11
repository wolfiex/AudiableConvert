

import os, json, time, sys, hashlib, requests, re, js2py
from p_tqdm import p_map


file = sys.argv[1]
out = '/Users/danielellis/Music/'



def get_key(file):
    ''' 
    A function to get the relevant checksum for Audiable
    '''

    # uint8Array
    filebuffer = open(file,'rb').read()[653: 653 + 20] 
    get_cs = '''
    function (bf) { 
        const buffer = new Uint8Array(bf)

        return Array.prototype.map.call(buffer, function (x) {
            return ('00' + x.toString(16)).slice(-2)}
        ).join('');  
        }'''

    get_cs_fn = js2py.eval_js(get_cs)
    checksum = get_cs_fn(list(filebuffer))

    assert re.match('[a-f0-9]{40}', checksum)
    res = requests.get("https://aax.api.j-kit.me/api/v2/activation/" + 
    checksum).json()
    print(res)

    return res['activationBytes']


#  set the parameters 
key = get_key(file)
name = os.path.basename(file).split('.')[0]
outfile = out+name+'/'
os.system('mkdir -p '+outfile)


# read the chapters
chapters = json.loads(os.popen(f'ffprobe -i {file} -print_format json -show_chapters -loglevel error').read())['chapters']

# convert seconds into timecode
hhmmss = lambda x: time.strftime('%H:%M:%S', time.gmtime(float(x)))

def writechapter(ch):
    os.popen(f'ffmpeg -activation_bytes {key} -ss {hhmmss(ch["start_time"])} -to {hhmmss(ch["end_time"])} -i {file} -metadata title="{ch["tags"]["title"]}" -codec copy {outfile}ch{ch["id"]}_{name}.m4b -y -loglevel quiet -stats')



p_map(writechapter, chapters)



