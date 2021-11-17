import sys
import os
import shutil

def Start():
    DeleteCount = 0

    folders = ["__pycache__"]
    DeleteCount = RecursiveDeleteFolder("..", folders)
    print(f"Deleted {DeleteCount} folders")
    DeleteCount = 0
    DeleteCount = DeleteLogs()
    print(f"Deleted {DeleteCount} logs")

def DeleteLogs() -> int:
    count = 0
    path = f"../../logs"
    for file in os.listdir(path):
        os.remove(path + "/" + file)
        print(f"Deleted {path}/{file}")
        count += 1
    return count

def RecursiveDeleteFolder(path: str, folders: list[str]) -> int:
    count = 0
    for file in os.listdir(path):
        if os.path.isdir(path + "/" + file):
            if file in folders:
                shutil.rmtree(f"{path}/{file}")
                print(f"Deleted {path}/{file}")
                count += 1
            else:
                count += RecursiveDeleteFolder(f"{path}/{file}", folders)
    return count

if __name__ == "__main__":
    Start()
