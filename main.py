
import os
import shutil


def create_subfolder(folder_path, sub_name):
    sub_path = os.path.join(folder_path, sub_name)
    if not os.path.exists(sub_path):
        os.mkdir(sub_path)
    return sub_path

def clean(folder_path):
    
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            print(os.path.join(folder_path, filename))
            file_ext = filename.split('.')[-1].lower()
            if file_ext:
                sub_name = f"{file_ext.upper()} files"
                sub_path = create_subfolder(folder_path, sub_name)
                file_path = os.path.join(folder_path, filename)
                new_location = os.path.join(sub_path, filename)
                if not os.path.exists(new_location):
                    shutil.move(file_path, sub_path)
                    print(f"moved: {filename} - > {sub_name}")
                else:
                    print(f"skipped : {filename}already exist iin {sub_name}")
        

if __name__ == '__main__':
    folder_path = 'C:/Users/user/Desktop/test'
    if os.path.isdir(folder_path):
        clean(folder_path)
        print('clean completed')
    else:
        print("fodler path does not exist")