from tkinter import Tk, Entry, END, mainloop, StringVar, Label, OptionMenu, Button

class Input_Terminal():
    def __init__(self):
        self.__master = Tk()
        self.__master.protocol("WM_DELETE_WINDOW", self.kill)

    def kill(self):
        self.__master.quit()
        self.__master.destroy()

    def main(self, get_parameters, set_parameters):
        master = self.__master

        scale, delta, k, ddepth, gaus_matrix, gaus_var, weight_alpha, weight_beta, weight_gamma, im_scale = get_parameters()

        numerical_input_text = ["scale", "delta", "k", "gaus matrix dim", "gaus scale?", "weight alpha", "weight beta", "weight gamma", "Output image scale"]
        numerical_inputs = [scale, delta, k, gaus_matrix[0], gaus_var, weight_alpha, weight_beta, weight_gamma, im_scale]

        numerical_input_boxes = [Entry(master, width=5) for n in range(len(numerical_input_text))]
        for n, (num_in_box, num_in, num_in_text) in enumerate(zip(numerical_input_boxes, numerical_inputs, numerical_input_text)):

            num_in_box.insert(END, num_in)
            num_in_box.grid(row=n, column=1)

            labelText=StringVar()
            labelText.set(num_in_text)
            labelDir=Label(master, textvariable=labelText, height=1)
            labelDir.grid(row=n, column=2)

        inputDepth = StringVar(master)
        inputDepth.set("cv2.CV_16S") # default value

        depthMenu = OptionMenu(master, inputDepth, "cv2.CV_8U", "cv2.CV_16U", "cv2.CV_16S", "cv2.CV_32F", "cv2.CV_64F")
        depthMenu.grid(row=len(numerical_inputs), column=1)
        labelText=StringVar()
        labelText.set("input depth")
        labelDir=Label(master, textvariable=labelText, height=1)
        labelDir.grid(row=len(numerical_inputs), column=2)

        update_button = Button(master, text="update parameters", command=lambda:self.update_parameters(numerical_input_boxes, inputDepth, get_parameters, set_parameters))
        update_button.grid(row=len(numerical_inputs)+1, column=1)

        mainloop()

    def update_parameters(self, boxes, menu, get_parameters, set_parameters):
        if get_parameters is None:
            print("No function for getting default parameters")
            return
        if set_parameters is None:
            print("No function for setting parameters")
            return

        scale, delta, k, ddepth, gaus_matrix, gaus_var, weight_alpha, weight_beta, weight_gamma, im_scale = get_parameters()

        new_inputs = [scale, delta, k, gaus_matrix, gaus_var, weight_alpha, weight_beta, weight_gamma, im_scale, ddepth]
        inputs = [box.get() for box in boxes]


        for ind, value in enumerate(inputs):

            if ind == 2:
                if value.isdigit():
                    val = int(value)
                    if val%2==1 and val < 32:
                        new_inputs[ind] = val
                continue #skriv ut error?

            if ind == 3:
                if value.isdigit():
                    val = int(value)
                    if val%2==1:
                        new_inputs[ind] = (int(value), int(value))
                continue #skriv ut error?

            try:
                val = float(value)
            except ValueError:
                continue #skriv ut error?

            if val < 0: continue #skriv ut error?

            if ind == 0 and val == 0: continue #skriv ut error?

            if ind == len(new_inputs)-2 and val == 0: continue #skriv ut error?

            new_inputs[ind] = val

        new_inputs[-1] = menu.get()
        #print("scale=1, delta=0, k=3, ddepth=cv2.CV_16S, gaus_matrix=(3,3), gaus_var=0, weight_alpha=.5, weight_beta=.5, weight_gamma=0, im_scale=1")
        #print(new_inputs[0] ,new_inputs[1], new_inputs[2], new_inputs[-1], new_inputs[3], new_inputs[4], new_inputs[5], new_inputs[6], new_inputs[7], new_inputs[7])
        set_parameters(new_inputs[0] ,new_inputs[1], new_inputs[2], new_inputs[-1], new_inputs[3], new_inputs[4], new_inputs[5], new_inputs[6], new_inputs[7], new_inputs[8])