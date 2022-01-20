import cv2

class ScreenCapure():
    def __init__(self, name_in='input', name_out='output'):
        self.__name_in = name_in
        self.__name_out = name_out
        self.__cam = cv2.VideoCapture(0)
        cv2.namedWindow(self.__name_in)
        cv2.namedWindow(self.__name_out)
        try:
            self.get_feed()
        except Exception as e:
            print(e)
            raise
        print("Frame grabbed")

        self.set_parameters()

    def get_feed(self):
        self.__ret, self.__frame = self.__cam.read()
        if not self.__ret:
            raise ConnectionError("failed to grab frame")
            #return 0

    def update(self):
        self.get_feed()
        edges = self.find_edges(self.__frame)

        edges = self.scale_image(edges, self.__im_scale)#skala upp och ned för att se hur mycket som tappas
        self.__edges = self.scale_image(edges, 1/self.__im_scale)
        #self.__edges = (255-self.__edges)

        cv2.imshow(self.__name_in, self.__frame)
        cv2.imshow(self.__name_out, self.__edges)

    def scale_image(self, im, scale):
        x = im.shape[1]
        y = im.shape[0]
        return cv2.resize(im, (int(x*scale), int(y*scale)))

    def find_edges(self, frame):
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_grey, self.__gaus_matrix, self.__gaus_var)

        grad_x = cv2.Sobel(img_blur, self.__ddepth, 1, 0, ksize=self.__k, scale=self.__scale, delta=self.__delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(img_blur, self.__ddepth, 0, 1, ksize=self.__k, scale=self.__scale, delta=self.__delta, borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        edges = cv2.addWeighted(abs_grad_x, self.__weight_alpha, abs_grad_y, self.__weight_beta, self.__weight_gamma)
        return edges

    def save_latest(self, savename='img/webcamscreencap.png'):
        #resize(src, dst, Size(), factor, factor, interpolation)
        cv2.imwrite(savename, self.__frame)

    def get_frame(self):
        return self.__frame

    def set_parameters(self, scale=1, delta=0, k=3, ddepth="cv2.CV_16S", gaus_matrix=(3,3), gaus_var=0, weight_alpha=.5, weight_beta=.5, weight_gamma=0, im_scale=1):
        self.__scale = scale
        self.__delta = delta
        self.__k = k
        self.__ddepth = exec(ddepth)
        self.__gaus_var = gaus_var
        self.__gaus_matrix = gaus_matrix
        self.__weight_alpha = weight_alpha
        self.__weight_beta = weight_beta
        self.__weight_gamma = weight_gamma
        self.__im_scale = im_scale

    def get_parameters(self):
        return self.__scale, self.__delta, self.__k, self.__ddepth, self.__gaus_matrix, self.__gaus_var, self.__weight_alpha, self.__weight_beta, self.__weight_gamma, self.__im_scale


    def kill(self, verbose=True):
        if verbose: print("Escape hit, closing...")

        self.__cam.release()
        cv2.destroyAllWindows()
