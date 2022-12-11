'''
This is the default execution procedure. 
It finds all .aax files in directory and converts them into mp3 files.

'''

try: from . import acfunctions as fns
except ImportError: import acfunctions as fns #testing  mode
import glob, os, sys

# we have not yet defined an activation key. 
key = False

dir = os.path.dirname( sys.argv[1] )
if dir[-1] != '/': dir += '/'
files = glob.glob(dir+'*.aax')
print(sys.argv,dir,len(files))


out = os.path.expanduser('~/Music')

if not key: 
    # extract the activation key. 
    try: from . import activation
    except ImportError: import activation
    key = activation.get_key(files[0])


for file in files:
    
    print('Converting file:', file)

    fns.convert(file, key, out)




print('Finished converting all files')



'''
From Audible Library, 
Show 50

var books = [...document.querySelectorAll('a.bc-button-text[href^="/library/download"]')];

books.forEach(async (d,i)=>{await new Promise(r => setTimeout(r, i*20000));console.log(i,'/',books.length); d.click()})

'''

'''
Usage instructions:

python -m AudiableConvert '/Users/xxxx/audiablebooks/'

'''