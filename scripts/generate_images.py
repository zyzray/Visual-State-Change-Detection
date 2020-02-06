import os
import cv2
import argparse

folder_name = 'data/fry_images/'


def video2img(video_path, kki):
    pic_folder = folder_name + str(kki) +'/'
    os.makedirs(pic_folder,exist_ok=True)
    vc = cv2.VideoCapture(video_path) 
    c=0
    rval=vc.isOpened()

    while rval: 
        c = c + 1
        rval, frame = vc.read()
        if rval:
            cv2.imwrite(pic_folder + str(kki) + '_' + str(c) + '.jpg', frame) 
            cv2.waitKey(1)
        else:
            break
    vc.release()
    print('save_success')
    print(pic_folder)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-kki',default=None,type=int)
	args = parser.parse_args()

	recipe_path = '/mnt/data/tasty_data/ALL_RECIPES/' 
	all_recipes = [all_recipes.rstrip('\n') for all_recipes in open( '/mnt/data/tasty_data/ALL_RECIPES.txt')]
	kki = args.kki
	print(' [*] ', kki, ' ', all_recipes[kki] )

	src_video = recipe_path +   all_recipes[kki]   +'/' +   'recipe_video.mp4'
	video2img(src_video, kki)
