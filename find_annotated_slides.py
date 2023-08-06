# Find and PDF annotated slides within a video by reading frames
# and detecting change based on file size difference

from pathlib import Path
from natsort import natsorted # natural sorting library. pip install natsort. https://pypi.org/project/natsort/
from PIL import Image # image processing library. pip install Pillow. https://pillow.readthedocs.io/en/stable/installation.html
import cv2 # image processing library. pip install opencv-python. https://pypi.org/project/opencv-python/

VIDEO_PATH = r'C:\Recordings'
FILE_SIZE_DIFFERENCE = 3000
INSIGNIFICANT_CHANGE = 2000
FRAME_INTERVAL = 20

def main():
    workDir = Path('.')
    videoDir = Path(VIDEO_PATH)
    imageDir = workDir / 'images'
    pdfDir = workDir / 'pdfs'
    executeList(videoDir, imageDir, pdfDir)
    print("Done")

def executeList(videoDir, imageDir, pdfDir):
    if videoDir.exists():
        videosList = (v for v in videoDir.glob('*.mp4'))
        imageDir.mkdir(exist_ok=True)
        pdfDir.mkdir(exist_ok=True)
        for video in videosList:
            print(f'--- VIDEO: {video.name} ---')
            clearImageDir(imageDir)
            nframes = extractImages(video, imageDir) # read video and screenshot frames
            if nframes:
                annotationFileSet = findAnnotations(imageDir) # find annotated slides
                pdfAnnotations(str(video.stem), annotationFileSet, pdfDir) # pdf annotated slides
            else:
                print('ERROR: No frames found.. CHECK video.')
    else:
        print('No videos found in video folder.')

def displayNicely(f):
    def inner(*args, **kwargs):
        print(f'Starting {f.__name__}..')
        inner_return = f(*args, **kwargs)
        print(f'Finished {f.__name__}..')
        return inner_return
    return inner

@displayNicely
def clearImageDir(imageDir:Path):
    for f in imageDir.glob('*.jpg'): # clear tmp image frames before processing next video
        f.unlink()

# https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
@displayNicely
def extractImages(video:Path, imageDir:Path):
    count = 0
    vidcap = cv2.VideoCapture(str(video.resolve()))
    success, image = vidcap.read()
    success = True
    n = 1 # number of total frames captured
    while success: # continues until no more frames are remaining in video
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
        success, image = vidcap.read()
        if not success:
            return (n-1)
        curImage = str((imageDir / f"frame{count}.jpg").resolve())
        cv2.imwrite(curImage, image)  # save frame as JPEG file
        count += FRAME_INTERVAL  # capture a frame every FRAME_INTERVAL seconds
        n += 1
    return n-1

# Filter by detection of significant changes between slides based on a file size range
@displayNicely
def findAnnotations(imageDir):
    i = 1
    newSize = 0
    lastFile = None
    tmphighest = None
    annotationFileSet = set()
    files = natsorted(imageDir.glob('*.jpg'))
    for file in files:
        fsize = file.stat().st_size
        if abs(fsize - (newSize)) > FILE_SIZE_DIFFERENCE:
            if tmphighest:
                if abs(tmphighest[-1] - fsize) < INSIGNIFICANT_CHANGE:
                    #tmp - store potential highest
                    tmphighest = (file, fsize)
            newSize = fsize
            if lastFile:
                annotationFileSet.add(lastFile)
            annotationFileSet.add((file, fsize))
        lastFile = (file, fsize)
        tmphighest = (file, fsize)
        i += 1
    return annotationFileSet

@displayNicely
def pdfAnnotations(videoName, imageSet, pdfDir):
    imagePaths = natsorted(e[0] for e in imageSet)
    pdfFilePath = pdfDir / (videoName+'.pdf')
    Image.open(imagePaths[0]).save(pdfFilePath, "PDF", resolution=1000.0, save_all=True, append_images=(Image.open(f) for f in imagePaths[1:]))
    
if __name__=="__main__":
    main()