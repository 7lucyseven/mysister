import hashlib

def is_new(lucy_hash):
    lucy_text = r'C:\Users\Creator\Desktop\mysister\lucy_voice\lucy_text.txt'
    f = open(lucy_text, 'rb')
    filedata = f.read()
    newhash = hashlib.md5(filedata).hexdigest()
    if(lucy_hash == newhash):
        return False
    else:
        return True

def get_voicetext():
    lucy_text = 'C:\\Users\\Creator\\Desktop\\mysister\\lucy_voice\\lucy_text.txt'
    with open(lucy_text, 'r', encoding='UTF-8') as f:
        datalist = f.readlines()
        return datalist[-1]
    