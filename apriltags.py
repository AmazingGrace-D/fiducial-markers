# Imports
import apriltag
import argparse
import cv2

# CLI arguments
ap = argparse.ArgumentParser()

ap.add_argument('-i', '--image', required=True,
                help='path to input image')

args = vars(ap.parse_args())

print('[INFO] loading image...')
image = cv2.imread(args['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# define the Apriltag detector options and then detetct the
# Apriltags in the input image

print('[INFO] Detecting AprilTags...')
options =apriltag.DetectorOptions(families='tag36h11')
detector = apriltag.Detector(options)
results = detector.detect(gray)
print('[INFO] {} total AprilTags detected'.format(results))


# loop over the results and display them

for r in results:
    # we extract the bounding box (x, y)-coordinates for the AprilTag
    # convert each of the (x, y)-coordinates pairs to ints
    (ptA, ptB, ptC, ptD) = r.corners
    ptB = (int(ptB[0]), int(ptB[1]))
    ptD = (int(ptD[0]), int(ptD[1]))
    ptC = (int(ptC[0]), int(ptC[1]))
    ptA = (int(ptA[0]), int(ptA[1]))


    # we draw the bounding box of the AprilTag detection
    cv2.line(image, ptA, ptB, (0, 255, 0), 2)
    cv2.line(image, ptB, ptC, (0, 255, 0), 2)
    cv2.line(image, ptC, ptD, (0, 255, 0), 2)
    cv2.line(image, ptD, ptA, (0, 255, 0), 2)

    # draw the centr (x, y)-coordinatez of the AprilTag
    (cX, cY) = (int(r.center[0]), int(r.center[1]))
    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

    # draw the tag fanmily on the image
    tagFamily = r.tag_family.decode("utf-8")
    cv2.putText(image, tagFamily, (ptA[0], ptA[1] -15), 
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0),2)

    print('[INFO] tag family: {}'.format(tagFamily))


# show output image after tag detection
cv2.imshow("Image", image)
cv2.waitKey(0)


