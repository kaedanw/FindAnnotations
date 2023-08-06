# FindAnnotations

Find and PDF annotated slides within a video by reading frames
and detecting change based on file size difference

Useful for following the conversation or discussion of lecture slides
which contain annotations/drawings/markings in a recorded video
but you have no access to the final annotated pdf.

Limitations:
- Currently, requires changing the folder of videos/recordings inside the script
  (Modifying and implementing command line arguments should be fairly straightforward however)
- Resulting PDF is compilation of images and text cannot be searched
- The capture interval and buffer window parameters are a tradeoff between
  extra processing time, missed frames, and irrelevant content
- The detection of change in slides is based on file size difference which
  is a simple but 'good enough' method for the purpose
  However, this more than often will capture additional irrelevant slides due
  to mouse movement, context windows clicked, webcam movement, etc..