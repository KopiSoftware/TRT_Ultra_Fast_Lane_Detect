import os
 
path ='Tusimple/clips'
 
def get_filelist(dir):
    for home, dirs, files in os.walk(path):
        for filename in files:
            if filename == "20.jpg" or filename == "20.png":
                continue
            else:
                print(filename)
                os.remove(os.path.join(home, filename))
 
if __name__ =="__main__":
    get_filelist(path)
