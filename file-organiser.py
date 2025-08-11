import os
import shutil
from os.path import splitext, exists, join



audio_ext = [".mp3", ".wav", "flac", ".m4a"]
image_ext = [".jpg", ".jpeg", ".png", ".svg", ".avif", ".webp", ".gif"]
video_ext = [".mp4", ".mp4v",  ".mpeg", ".avi"]
document_ext = [".pptx", ".txt",".pdf", ".docx", ".doc", ".ppt"]




def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter +=1

    return name


def move(dest, file, name):
 
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest,name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        print(oldName, newName)
    shutil.move(file, dest)



def create_subfolder(folder_path, sub_name):
    sub_path = os.path.join(folder_path, sub_name)
    if not os.path.exists(sub_path):
        os.mkdir(sub_path)
    return sub_path

def clean(folder_path):
    
       with os.scandir(folder_path) as files:
            for file in files:
                name = file.name
                file_ext = name.split('.')[-1].lower()
                print(os.path.join(folder_path, name))
                print(file_ext)
                for image in image_ext:      
                    if name.endswith(image) or name.endswith(image.upper()):
                         sub_name = f"image files"
                         sub_path = create_subfolder(folder_path, sub_name)
                         file_path = os.path.join(folder_path, name)
                         new_location = os.path.join(sub_path, name)
                         move(new_location, file, name)
                        
                for document in document_ext:      
                    if name.endswith(document) or name.endswith(document.upper()):
                         sub_name = f"document files"
                         sub_path = create_subfolder(folder_path, sub_name)
                         file_path = os.path.join(folder_path, name)
                         new_location = os.path.join(sub_path, name)
                         if not os.path.exists(new_location):
                            shutil.move(file_path, sub_path)
                            print(f"moved: {name} - > {sub_name}")
                         else:
                            print(f"skipped : {name}already exist iin {sub_name}")





if __name__ == '__main__':
    folder_path = 'C:/Users/user/Desktop/test'
    if os.path.isdir(folder_path):
        clean(folder_path)
        print('clean completed')
    else:
        print("fodler path does not exist")