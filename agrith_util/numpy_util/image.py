#!/usr/bin/env python
# coding=utf-8
from PIL import Image
import numpy as np

def test():
    im = Image.open('test.jpg')
    im.show()
    print im.mode, im.size, im.format
    im_numpy = np.asarray(im) # 把读入的图片作为矩阵
    print im_numpy.shape  # 图片矩阵的shape信息

    box = (100, 100, 200, 200)
    region = im.crop(box)
    region.show()
    region = region.transpose(Image.ROTATE_180)
    region.show()
    im.paste(region, box)
    im.show()
    im.save('t.jpg')
def save(outfile):
    try:
        Image.save(outfile)
    except IOError:
        print("cannot save", outfile)

if __name__=='__main__':
    test()
