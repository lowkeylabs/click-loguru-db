# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:44:27 2017

@author: jleonard99
"""

# pylint: disable-all

import os
import cv2
import screeninfo
import imutils

import click
from loguru import logger
from src import click_config_file,myprovider

logger.trace(f"After imports {__file__}")

def display_pics( screen_id,image_folder ):
    ''' display pictures from folder in full screen '''
    is_color = True

    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    (width, height) = (screen.width, screen.height)

    if not os.path.exists( "C:\\Users\\john\\.my-setup\\Background1.jpg" ):
        print("die")

    #image = cv2.imread("C:\\Users\\john\\.my-setup\\Background1.jpg",cv2.IMREAD_COLOR)

    images = [
        'https://images.unsplash.com/photo-1537979513163-d64bf250f08a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
        'https://images.unsplash.com/photo-1537819191377-d3305ffddce4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1121&q=80'
    ]

    i = 0
    while True:
        url = images[i]
        image = imutils.url_to_image(url)

        window_name = 'projector'
        winprop =  cv2.WND_PROP_FULLSCREEN

        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN )
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN )
        cv2.imshow(window_name, image)

        if cv2.waitKey(1500) & 0xFF == ord('q'):
            break

        i = i + 1
        if i > len(images)-1:
            i = 0

    cv2.destroyAllWindows()

@click.command()
@click.option('--image-folder', help='folder with images to display')
@click.option('--screen-id', default=1, help='For multimonitor systems, use this screen ID')
#@click_config_file.configuration_option()
@click_config_file.configuration_option(implicit=True,provider=myprovider)
def cli(image_folder,screen_id):
    """ Slides show images in full screen """
    logger.debug(f"Entering {os.path.basename(__file__)[:-3]}")
    logger.trace(f"screen_id : {screen_id}")
    logger.trace(f"image_folder: {image_folder}")
    display_pics( screen_id, image_folder )


if __name__ == '__main__':
    cli()
