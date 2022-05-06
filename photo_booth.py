from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
import time


import cv2
import image_processing

global edges_image

# may allah forgive me for how I am dealing with the images

def remake_edges(blur_radius = 11, lower_thresh = 0, upper_thresh = 20, aperture_size = 3, bind_dist = 10, area_cut = 3,
        min_len = 20, calc_rogues = False, blur_radius_shade = 21, line_dist = 5, theta = None, bind_dist_shade = 10, area_cut_shade = 10,
        min_len_shade = 15, thresholds = [10, 30, 50, 80]):
    """
    Remakes the edges image using the given parameters.
    """
    filename = "image.png"
    frame = cv2.imread(filename)

    segments = image_processing.process_combo_raw(frame, blur_radius, lower_thresh, upper_thresh, aperture_size, bind_dist, area_cut, min_len, calc_rogues, blur_radius_shade, line_dist, theta, bind_dist_shade, area_cut_shade, min_len_shade, thresholds) #if this line is wrong its github copilots fault
    #     segments = trajectory_planning.calc_path(segments, 5, .01, 1, 120)
    edges_image = image_processing.plot_segments(segments)

    cv2.imwrite("edges_image.jpg", edges_image)
    time.sleep(.1)


class MainWindow(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("image.png")

        print("Captured")
        remake_edges()







class SecondWindow(Screen):
    pass

class AjustmentWindow(Screen):
    def update_values(self):
        remake_edges(blur_radius= self.blur_radius.value, upper_thresh=self.edge_sensitivity.value, min_len= self.min_len.value)

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("photo_booth.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()