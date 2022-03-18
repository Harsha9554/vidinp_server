import torch, torchvision

import detectron2

# import some common libraries
import numpy as np
import cv2
from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo # load a model from COCO model ZOO
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

from google.colab import drive
import cv2
import time
from scipy import ndimage


def process_vid(actual_vid):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_DC5_1x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_DC5_1x.yaml")
    
    predictor = DefaultPredictor(cfg)
    
    
    # open video stream
    cap = cv2.VideoCapture(r'/content/drive/MyDrive/Prism/take_noob_3.MOV') # change as appropriate
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    current_frame = 0
    
    # rescale for better performances
    WIDTH = cap.get(3)
    print(WIDTH)
    HEIGHT = cap.get(4)
    print(HEIGHT)
    FPS = cap.get(5)
    SCALE_RATIO = 59 # percent from original size
    
    SCALED_WIDTH = int(WIDTH * SCALE_RATIO / 100)
    SCALED_HEIGHT = int(HEIGHT * SCALE_RATIO / 100)
    
    DIM = (SCALED_WIDTH, SCALED_HEIGHT)
    DIM = (1920, 1080)
    print("Resizing to: ", DIM)
    
    #cv2.startWindowThread()
    
    # writing the output to a video
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, DIM)
    
    n_frame = 0
    
    # first frame is too dark, taking the 19th frame as anchor point
    while True:
        _, frame = cap.read()
        n_frame += 1
    
        if n_frame == 20:
            # frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = cv2.resize(frame, DIM)
            first_frame = frame
            break
    
    cv2_imshow(first_frame)
    
    try:
      while True:
          
          print("Processing frame %s of %s" %(current_frame, total_frames), flush=True)
          
          # Capture frame-by-frame
          _, frame = cap.read()
    
          # resizing for faster detection
          # frame = cv2.rotate(frame, cv2.ROTATE_180)
          frame = cv2.resize(frame, DIM)
          
    
          # using a greyscale picture, also for faster detection
          gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
          # detect people in the image
          
          # returns the bounding boxes for the detected objects
          outputs = predictor(frame)
          outputs = outputs["instances"].pred_boxes.to('cpu').tensor.numpy().astype(int)
    
          # iterate over each detected person and
          # substitute the area with the first frame
          original = frame.copy()
          rectangle = frame.copy()
          
          for (x, y, w, h) in outputs:
    
              crop_img = first_frame[y:y + h, x:x + w]
              frame[y:y + h, x:x + w] = crop_img
              
              # could also write
              # frame[y:y + h, x:x + w] = first_frame[y:y + h, x:x + w]
    
              # for debugging show bounding rectangle
              cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)
              cv2.rectangle(rectangle, (x, y), (x+w, y+h), (0, 255, 0), 2)
              
          #cv2_imshow(frame)
          out.write(frame)
          
          # also for debugging
          # cv2_imshow(frame)
          # cv2_imshow('First Frame', first_frame)
          # cv2_imshow('CLean Frame', original)
          # cv2_imshow('Rectangle Frame', rectangle)
          print('Writing to frame')
          
          
          current_frame += 1
          
          del(frame, gray, outputs, original, rectangle) # empty memory
          
          if current_frame == total_frames:
              break
    
      # and release the output
      out.release()
    
      cap.release()
      cv2.destroyAllWindows()
      cv2.waitKey(1)
    except:
      print("Completed")