#GUI프로그램 시작

from fileinput import filename
from tkinter import *
from tkinter import filedialog
import torch
import makeLineDrawing

root = Tk()
root.title('Line Drawing')
 
filename

def open():
    # global my_image
    global filename
    filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=[
                    ("all video format", ".mp4"),
                    ("all video format", ".flv"),
                    ("all video format", ".avi"),
                ])
    
    Label(root, text=filename).grid(row=1, column=0, padx=10, pady=10) # 파일경로 view
    # my_image = ImageTk.PhotoImage(Image.open(root.filename))
    # Label(image=my_image).grid(row=6, column=0, padx=10, pady=10) #사진 view

def videoMat():
    model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3").cuda() # or "resnet50"
    convert_video = torch.hub.load("PeterL1n/RobustVideoMatting", "converter")
    print("file path = " + filename)
    convert_video(
        model,                           # The loaded model, can be on any device (cpu or cuda).
        input_source='bwl.mp4',        # A video file or an image sequence directory.
        downsample_ratio=None,           # [Optional] If None, make downsampled max size be 512px.
        output_type='video',             # Choose "video" or "png_sequence"
        output_composition='matted.mp4',    # File path if video; directory path if png sequence.
        output_alpha="pha.mp4",          # [Optional] Output the raw alpha prediction.
        output_foreground="fgr.mp4",     # [Optional] Output the raw foreground prediction.
        output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
        seq_chunk=12,                    # Process n frames at once for better parallelism.
        num_workers=1,                   # Only for image sequence input. Reader threads.
        progress=True                    # Print conversion progress.
    )

def makeLineDraw():
    videoMat()
    makeLineDrawing.start()

##################### 
Label(
    root,
    text='Line Drawing을 생성하기 위한 파일을 선택하세요'
).grid(row=0, column=0, padx=10, pady=10)
my_btn = Button(root, text='영상파일 열기', command= lambda : open()).grid(row=0, column=1, padx=10, pady=10)
 
my_btn = Button(root, text='백그라운드 제거 및 라인드로잉 생성', command= lambda : makeLineDraw()).grid(row=2, column=0, padx=10, pady=10)

# my_btn = Button(root, text='라인드로잉 생성', command=exec("Script1.py")).grid(row=3, column=0, padx=10, pady=10)
 
root.mainloop()