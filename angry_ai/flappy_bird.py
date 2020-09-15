import cv2
cap = cv2.VideoCapture('angry_ai/intro2.mkv')
def rescale_frame(frame, percent=75):
  width = 570
  height = 670
  dim = (width, height)
  return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
if (cap.isOpened()== False):
  print("Error opening video stream or file")
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame150 = rescale_frame(frame, percent=150)
        cv2.imshow("Fllapy Bird Game - S&M's", frame150)
#
        # cv2.imshow('Frame', frame)
#
        if cv2.waitKey(25) & 0xFF == ord('\x0D') or (cv2.waitKey(25) & 0xFF == ord('\x20')):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
from main_screen import Game
g = Game()
while g.running:
    g.curr_menu.display_menu()

