# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 21:30:49 2019

@author: fame
"""

import xml.etree.ElementTree as ET
from os import walk
import os
import pickle 
import numpy as np
from tqdm import *
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import argparse


def read_steps(cat_root):
    data_dict = {}
    cats = cat_root.findall('steps_updated')
    assert( cats != None )

    categories = cats[0].findall('steps_updated')
    assert( categories != None )

    data_dict = []
    for cat in categories:
        currsts = cat.text
        currsts = re.sub(r'[^\w\s]','',currsts) 
        data_dict.append( currsts.split()  )
    return data_dict

 
def read_label_frames(recipe_steps, annotation_steps):

    frame_labels = []
    for xi in range (0, len(recipe_steps) ):
        if annotation_steps[xi] == '-1,-1':
            curr_range = []
        else:
            annots = annotation_steps[xi].split(',')
            start_frame = int(annots[0] )
            end_frame = int(annots[1])
            if start_frame == 1:
                start_frame_actual = 1
            else:
                start_frame_actual = start_frame*5 - 4
            end_frame_actual = end_frame*5

            curr_range = (start_frame_actual, end_frame_actual) #can modify, be careful 

        frame_labels.append(curr_range)
    return frame_labels
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-kki',default=None,type=int)
    args = parser.parse_args()


    recipe_path = '/mnt/data/tasty_data/ALL_RECIPES/' 
    all_recipes = [all_recipes.rstrip('\n')    for all_recipes  in open( '/mnt/data/tasty_data/ALL_RECIPES.txt')]

    curr_els = 'fry' # modify here to change element
    all_sent_frame_list = []
    kki = args.kki
    print(' [*] ', kki, ' ', all_recipes[kki] )
    
    rec_f =          recipe_path +   all_recipes[kki]   + '/' + "recipe.xml"
    src_annotation = recipe_path +   all_recipes[kki]   +  '/' +   'csvalignment.dat'
    annotation_steps =  [line.rstrip('\n') for line in open(src_annotation)]

    tree = ET.parse(rec_f)
    cat_root = tree.getroot()
    recipe_steps = read_steps(cat_root)
    recipe_annotations = read_label_frames(recipe_steps,   annotation_steps )

    src_video = recipe_path +   all_recipes[kki]   +'/' +   'recipe_video.mp4'
    fps_video = recipe_path +   all_recipes[kki]   +'/' +   'fps.txt'
    fps_video =  [line.rstrip('\n') for line in open(fps_video)]
    fps_video = float(fps_video[0])
    for kkirt in range(len(recipe_steps)): 
        flat_list = recipe_steps[kkirt] 

        if not curr_els in flat_list:
            continue
        if  len(recipe_annotations[kkirt] ) == 0 :
            continue
        
        allinds = [flat_list.index(curr_els)]
         
        current_directory =  'state_videos/fry_extended/'  
        if not os.path.exists(current_directory):
           os.makedirs(current_directory)

        video_name = current_directory +   str(kki) + '_extended' + str(kkirt)   + '.mp4' 
        startF = float(recipe_annotations[kkirt][0]) / fps_video
        startF -= 7
        startF = max(startF, 1)


        endF = float(recipe_annotations[kkirt][1]) /fps_video
        endF += 7
        clip = VideoFileClip(src_video)
        endF = min(endF, clip.duration)

        ffmpeg_extract_subclip(src_video, startF, endF , targetname=video_name)
    
 
