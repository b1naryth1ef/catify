import cv, requests, Image
from StringIO import StringIO

def detectFaces(image, faceCascade):
    #modified from: http://www.lucaamore.com/?p=638
    min_size = (20, 20)
    image_scale = 1
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Allocate the temporary images
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale), cv.Round(image.height / image_scale)), 8, 1)

    # Scale input image for faster processing
    cv.Resize(image, smallImage, cv.CV_INTER_LINEAR)

    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)

    # Detect the faces
    faces = cv.HaarDetectObjects(
        smallImage, faceCascade, cv.CreateMemStorage(0),
        haar_scale, min_neighbors, haar_flags, min_size)

    res = []
    for ((x, y, w, h), n) in faces:
        pt1 = (int(x * image_scale), int(y * image_scale))
        pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
        res.append((pt1, pt2))
    return res

def pil2cvGrey(pil_im):
    #from: http://pythonpath.wordpress.com/2012/05/08/pil-to-opencv-image/
    pil_im = pil_im.convert('L')
    cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0])
    return cv_im

def getCatImage(h, w):
    r = requests.get("http://placekitten.com/%s/%s" % (h, w))
    return Image.open(StringIO(r.content))

faceCascade = cv.Load('haarcascade_frontalface_default.xml')
def catify(img):
    cv_im = pil2cvGrey(img)
    res = detectFaces(cv_im, faceCascade)
    print "Faces Detected: %s" % len(res)
    for a, b in res:
        h, w = b[0]-a[0], b[1]-a[1]
        cat = getCatImage(h, w)
        img.paste(cat, (a[0], a[1]))
    return img
