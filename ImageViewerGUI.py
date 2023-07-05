from my_package.model import ImageCaptioningModel
from my_package.model import ImageClassificationModel
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.ttk import *


def fileClick(clicked):
    # Define the function you want to call when the filebrowser button (Open) is clicked.
    # This function should pop-up a dialog for the user to select an input image file.
    # To have a better clarity, please check out the sample video.
    file = filedialog.askopenfilename()
    clicked['file'].set(file)
    image = Image.open(file)
    image= image.resize((500,400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    for widgets in clicked['imageframe'].winfo_children():
        widgets.destroy()
    l1 = Label(clicked['imageframe'])
    l1.grid(row=0, column=0)
    l1.configure(image=img)
    l1.image = img

    pass


def process(clicked, captioner, classifier):
    # This function will produce the required output when 'Process' button is clicked.
    # Note: This should handle the case if the user clicks on the `Process` button without selecting any image file.
    if (clicked['file'].get() == ''):
        print("File not Selected")
        return

    if (clicked['dropdown'] == 'Caption'):
        captions = captioner(status['file'].get())
        for widgets in clicked['processframe'].winfo_children():
            widgets.destroy()
        f1 =Frame(clicked['processframe'], borderwidth=2,relief="solid")
        f1.grid(row=0,column=0,sticky="")
        l2 = Label(f1,text="Captions",font=("comicsans",19,"bold"))
        l2.grid(row=0, column=0)
        for i,c in enumerate(captions):
            l2 = Label(f1,text=c)
            l2.grid(row=i+1, column=0)

        pass
    elif (clicked['dropdown'] == 'Classification'):
        classification = classifier(status['file'].get())
        for widgets in clicked['processframe'].winfo_children():
            widgets.destroy()
        f1 =Frame(clicked['processframe'], borderwidth=2,relief="solid")
        f1.grid(row=0,column=0,sticky="")
        l2 = Label(f1,text="Classifications",font=("comicsans",19,"bold"))
        l2.grid(row=0, column=0)
        for i,c in enumerate(classification):
            l2 = Label(f1,text=c[1]+" : "+str(c[0]*100)+"%")
            l2.grid(row=i+1, column=0)
        pass
    pass


def processWrapper(status, combobox, captioner, classifier):
    status['dropdown'] = combobox.get()
    process(status, captioner, classifier)


if __name__ == '__main__':
    # Complete the main function preferably in this order:
    # Instantiate the root window.

    root = Tk()
    root.title("Software Lab|IIT KGP|Image Viewer|21CS10011")
    status = {'file': StringVar(), 'img': ""}
    filePath = Entry(root, width=50, textvariable=status['file'])
    filePath.grid(row=0, column=0)
    imageDisplay = Frame(root, width=500, height=400)
    imageDisplay.grid(row=1, column=0)
    imageDisplay.grid_rowconfigure(0, weight=1)
    imageDisplay.grid_columnconfigure(0, weight=1)
    status['imageframe'] = imageDisplay
    chooseImg = Button(root, text="Select Image",
                       command=lambda: fileClick(status))
    chooseImg.grid(row=0, column=1)
    processType = Combobox(root, state="readonly")
    processType['values'] = ("Caption", "Classification")
    processType.current(0)
    processType.grid(row=0, column=2)
    classifier = ImageClassificationModel()
    captioner = ImageCaptioningModel()
    processOutputDisplay = Frame(root,width=200,height=400)
    processOutputDisplay.grid(row=1, column=1,padx=5)
    processOutputDisplay.grid_rowconfigure(0, weight=1)
    processOutputDisplay.grid_columnconfigure(0, weight=1)

    status['processframe']=processOutputDisplay
    processButton = Button(root, text="Process", command=lambda: processWrapper(
        status, processType, captioner, classifier))
    processButton.grid(row=0, column=3)

    root.mainloop()
    # Provide a title to the root window.
    # Instantiate the captioner, classifier models.
    # Declare the file browsing button.
    # Declare the drop-down button.
    # Declare the process button.
    # Declare the output label.
    pass
