import os
from os.path import splitext, exists, join
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




source_dir=""


audio_ext = [".mp3", ".wav", "flac", ".m4a"]
image_ext = [".jpg", ".jpeg", ".png", ".svg", ".avif", ".webp", ".gif"]
video_ext = [".mp4", ".mp4v",  ".mpeg", ".avi"]
document_ext = [".pptx", ".txt",".pdf", ".docx", ".doc", ".ppt"]


def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        print(name)
        counter +=1
    return name


def move(dest, file, name):

    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest,name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        os.rename(oldName, newName)
    shutil.move(file, dest)

             
    


def create_subfolder(folder_path, sub_name):
    sub_path = os.path.join(folder_path, sub_name)
    if not os.path.exists(sub_path):
        os.mkdir(sub_path)
    return sub_path


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as files:
            for file in files:
                name = file.name
                self.check_audio_files(file, name)
                self.check_image_files(file, name)
                self.check_video_files(file, name)
                self.check_document_files(file, name)


    def check_audio_files(self, file, name):
        for audio in audio_ext:      
            if name.endswith(audio) or name.endswith(audio.upper()):
                if file.stat().st_size < 1500000 or "SFX" in name:
                    sub_name = f"audio files"
                    sub_path = create_subfolder(source_dir, sub_name)
                    new_location = os.path.join(sub_path, name)
                    move(new_location, file, name)
                else:
                    sub_name = f"sfx files"
                    sub_path = create_subfolder(source_dir, sub_name)
                    new_location = os.path.join(sub_path, name)
                    move(new_location, file, name)
            logging.info(f"Moved audio file: {name}")

    def check_video_files(self, file, name):
         for video in video_ext:        
            if name.endswith(video) or name.endswith(video.upper()):
                    sub_name = f"video files"
                    sub_path = create_subfolder(source_dir, sub_name)
                    new_location = os.path.join(sub_path, name)
                    move(new_location, file, name)
                    logging.info(f"Moved video file: {name}")
        
    def check_document_files(self, file, name):
         for document in document_ext:    
            if name.endswith(document) or name.endswith(document.upper()) :
                sub_name = f"document files"
                sub_path = create_subfolder(source_dir, sub_name)              
                new_location = os.path.join(sub_path, name)
                move(new_location, file, name)
                logging.info(f"Moved document file: {name}")



    def check_image_files(self, file, name):   
        for image in image_ext:       
            if name.endswith(image) or name.endswith(image.upper()):
                sub_name = f"image files"
                sub_path = create_subfolder(source_dir, sub_name)
                new_location = os.path.join(sub_path, name)
                move(new_location, file, name)
                logging.info(f"Moved image file: {name}")




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()