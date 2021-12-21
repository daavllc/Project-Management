# 
# Check update against GitHub file, and prompt for download
import logging
import os
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from multiprocessing import Process, current_process
from zipfile import ZipFile

import config.config as config

formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger("PM.Updater")
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
log.addHandler(sh)
if not os.path.exists(f"{config.PATH_ROOT}/logs"):
    os.mkdir(f"{config.PATH_ROOT}/logs")
fh = logging.FileHandler(filename=f"{config.PATH_ROOT}/logs/updater.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

class Var:
    org = "daavofficial"
    repo = "Project-Management"
    branch = "main"
    versionPath = "src/config/config.py"
    find = "VERSION = "
    token = None # for private repositories

def Check() -> bool:
    if os.path.exists(f"{config.PATH_ROOT}/FinishUpdate.py"):
        os.remove(f"{config.PATH_ROOT}/FinishUpdate.py")

    currentVersion = None
    localVersion = None
    response = None
    try:
        response = urllib.request.urlopen(f"https://raw.githubusercontent.com/{Var.org}/{Var.repo}/{Var.branch}/{Var.versionPath}")
    except urllib.error.HTTPError as e:
        log.warn(f"Unable to check version: {e}")
        print("Unable to check for update. Continuing...")
        return False

    content = response.read().decode("UTF-8")

    for line in content.split("\n"):
        if Var.find in line:
            currentVersion = line[len(Var.find):].strip('"')
            break

    if currentVersion is None:
        log.warn("Unable to find current version")
        return False

    currentVersion = GetIntVersion(currentVersion)
    localVersion = GetIntVersion(config.VERSION)
    difference = []
    for current, local in zip(currentVersion, localVersion):
        difference.append(current - local)
    for section in difference:
        if section < 0: # For future versions
            return False
        elif section > 0:
            print(f"A new version was found! ({GetStrVersion(currentVersion)})")
            if not 'n' in input(f"  Would you like to update from ({GetStrVersion(localVersion)})? (Y/n) "):
                return GetUpdate()
            break
    return False

def GetUpdate() -> bool:
    response = None
    try:
        response = urllib.request.urlopen(f"https://api.github.com/repos/{Var.org}/{Var.repo}/zipball/{Var.branch}")
    except urllib.error.HTTPError as e:
        log.warn(f"Unable to downlaod from GitHub: {e}")
        print("Unable to download update. Continuing...")
        input("Press enter to continue...")
        return False

    if not os.path.exists(f"{config.PATH_ROOT}/new"):
        os.mkdir(f"{config.PATH_ROOT}/new")
    os.chdir(f"{config.PATH_ROOT}/new") # Change directory to ROOT/new
    with open(f"{Var.repo}.zip", "wb") as f:
        f.write(response.read())
    
    # We now have a zip of the latest version
    zipFileContent = dict()
    zipFileContentSize = 0
    with ZipFile(f"{Var.repo}.zip", 'r') as zipFile:
        for name in zipFile.namelist():
            zipFileContent[name] = zipFile.getinfo(name).file_size
        zipFileContentSize = sum(zipFileContent.values())
        extractedContentSize = 0
        for zippedFileName, zippedFileSize in zipFileContent.items():
            UnzippedFilePath = os.path.abspath(f"{zippedFileName}")
            os.makedirs(os.path.dirname(UnzippedFilePath), exist_ok=True)
            if os.path.isfile(UnzippedFilePath):
                zipFileContentSize -= zippedFileSize
            else:
                zipFile.extract(zippedFileName, path="", pwd=None)
                extractedContentSize += zippedFileSize
            try:
                done = int(50*extractedContentSize/zipFileContentSize)
                percentage = (extractedContentSize / zipFileContentSize) * 100
            except ZeroDivisionError:
                done = 50
                percentage = 100
            sys.stdout.write('\r[{}{}] {:.2f}%'.format('█' * done, '.' * (50-done), percentage))
            sys.stdout.flush()
    sys.stdout.write('\n')
    os.chdir(f"{config.PATH_ROOT}")
    os.rename(f"{config.PATH_ROOT}/src/update/FinishUpdate.py", f"{config.PATH_ROOT}/FinishUpdate.py")
    pyPath = ""
    with open(f"{config.PATH_ROOT}/settings/launch.txt", 'r', encoding='utf-8') as f:
        pyPath = f.readlines()[0]
    print(pyPath)
    sys.exit(-1)

def GetIntVersion(version: str) -> list[int]:
    version = version.split(".")
    intVer = []
    for section in version:
        if section.isalnum():
            newSection = ""
            for char in section:
                if char.isnumeric():
                    newSection += char
            section = newSection
        intVer.append(int(section))
    return intVer

def GetStrVersion(version: list) -> str:
    strVer = ""
    for idx, section in enumerate(version):
        strVer += str(section)
        if idx < len(version) - 1:
            strVer += "."
    return strVer
