#!/usr/bin/env python
# coding=utf-8

from PIL import Image
import numpy as np

def rebuild_img(u, sigma, v, p): #p表示奇异值的百分比
    print p
    m = len(u)
    n = len(v)
    a = np.zeros((m, n))

    count = (int)(sum(sigma))
    curSum = 0
    k = 0
    while curSum <= count * p:
        uk = u[:, k].reshape(m, 1)
        vk = v[k].reshape(1, n)
        a += sigma[k] * np.dot(uk, vk)
        curSum += sigma[k]
        k += 1
    print 'k:',k
    a[a < 0] = 0
    a[a > 255] = 255
    #按照最近距离取整数，并设置参数类型为uint8
    return np.rint(a).astype("uint8")

if __name__ == '__main__':
    img = Image.open('test.jpg', 'r')
    a = np.array(img)

    for p in np.arange(0.1, 1, 0.1):
        u, sigma, v = np.linalg.svd(a[:, :, 0])
        R = rebuild_img(u, sigma, v, p)

        u, sigma, v = np.linalg.svd(a[:, :, 1])
        G = rebuild_img(u, sigma, v, p)

        u, sigma, v = np.linalg.svd(a[:, :, 2])
        B = rebuild_img(u, sigma, v, p)

        I = np.stack((R, G, B), 2)
        #保存图片在img文件夹下
        Image.fromarray(I).save("svd_" + str(p * 100) + ".jpg")
