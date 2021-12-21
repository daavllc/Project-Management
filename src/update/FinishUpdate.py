import shutil
import os

def main():
    print("Finishing update!")
    ROOT_PATH = __file__[:-16].replace('\\', '/')
    newPath = ""
    print(ROOT_PATH)
    for file in os.listdir(ROOT_PATH):
        if os.path.isdir(f"{ROOT_PATH}/{file}"):
            if file in ["src"]:
                shutil.rmtree(f"{ROOT_PATH}/{file}")
            if file == "new":
                for item in os.listdir(f"{ROOT_PATH}/{file}"):
                    if os.path.isdir(f"{ROOT_PATH}/{file}/{item}"):
                        newPath = f"{ROOT_PATH}/{file}/{item}"
        else: # files
            os.remove(f"{ROOT_PATH}/{file}")

    # Now everything but settings/user data is deleted

    for file in os.listdir(newPath):
        os.rename(f"{newPath}/{file}", f"{ROOT_PATH}/{file}")
    shutil.rmtree(f"{ROOT_PATH}/new")

if __name__ == "__main__":
    main()