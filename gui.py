import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import cv2
from PIL import Image, ImageTk
import inspect
from DCT import  DiscreteCosineTransform
global channel
from AES import AESCipher
container2wt = 0

def select_image():
    print('Select Image')
    global image_path
    image_path = tk.filedialog.askopenfilename(title="Select image", filetypes=[("all files", '*.*')])
    print(image_path)
    if (image_path):
        root.update_idletasks()
        global original_image_label
        load = Image.open(image_path)
        original_image = ImageTk.PhotoImage(load)
        print(type(original_image))
        original_image_label.config(image = original_image)
        original_image_label.image = original_image
        original_image_label.pack(in_=container2, fill=tk.BOTH, expand=True)

def select_secret_file():
    # global secret_image_path
    print("Select secret file")
    secret_file = tk.filedialog.askopenfile(title="Select file", filetypes=[("All files", '*.*')])
    # print(secret_image_path)
    data = secret_file.read()
    text1.insert(tk.END, data)

def clear_image():
    print('Save Image')
    # print(processed_image_label.image)
    clear_processed_image()

def exit_app():
    print('Exit App')
    messagebox = tk.messagebox.askyesno("Exit Application","Are you sure you want to exit?")
    print(messagebox)
    if (messagebox):
        root.quit()

def process():
    try:
        print('process()')
        encrypt_decrypt = options_clicked.get()
        algo_technique = technique_options_clicked.get()
        # Check for secret data
        secret_string = text1.get("1.0",tk.END)
        # check for carrier
        try: image_path
        except NameError:
            tk.messagebox.showwarning("Data Required","Please select carrier image to proceed")
            return
        # original_image = cv2.imread(image_path)
        print(secret_string)
        if (algo_technique == technique_options[0]):
            # DCT Algorithm
            dctAlgoStegano("DCT", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[1]):
            dctAlgoStegano("first_DCT", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[2]):
            dctAlgoStegano("AES_DCT", secret_string, encrypt_decrypt)
    except NameError as error:
        print(error)

def dctAlgoStegano(type, secret_string, encrypt_decrypt):
    outFile = "result/result.png"
    print(type)
    if (encrypt_decrypt == options[0]):
        if (len(secret_string) == 1):
            print("Empty Secret:: Showing warning")
            tk.messagebox.showwarning("Data Required", "Please enter secret data to be encoded")
            return
    if (type == "DCT"):
        if (encrypt_decrypt == options[0]):
            DCT = DiscreteCosineTransform(image_path)
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            dct_img_encoded = DCT.DCTEncoder(img, secret_string, channelchoose())
            cv2.imwrite(outFile, dct_img_encoded)    
            displayImage("result/result.png")    
        else:
            try:
                img2 = cv2.imread(outFile, cv2.IMREAD_UNCHANGED)
                DCT = DiscreteCosineTransform(image_path)
                msgbits = DCT.DCTDecoder(img2)
                a = msgbits.index(42)
                decoded = bytes(msgbits[a+1:])
                displaySecret(decoded.decode())
                #saveSecretToFile(decoded.decode())
            except:
                displaySecret("")
                tk.messagebox.showwarning('Falied To Extract The Message.','Try other ways or there is nothing in the picture!')
    elif (type == "first_DCT"):
        if (encrypt_decrypt == options[0]):
            outFile = "result/result.png"
            x = DiscreteCosineTransform(image_path)
            secret = x.DCTEn0(secret_string, outFile, channelchoose())
            print("secret :: DCT:: ",secret)
            # secret = red.hide(image_path, secret_string)
            # secret.save("secret.png")
            displayImage("result/result.png")
        else:
            try:
                y = DiscreteCosineTransform(image_path)
                secret = y.DCTDe()
                # secret = red.reveal(image_path)
                displaySecret(secret)
                #saveSecretToFile(secret)
            except:
                displaySecret("")
                tk.messagebox.showwarning('Falied To Extract The Message.','Try other ways or there is nothing in the picture!')
    elif (type == "AES_DCT"):
        if (encrypt_decrypt == options[0]):
            key = sp.get()
            #print(key)
            DCT = DiscreteCosineTransform(image_path)
            cipher = AESCipher(key.encode())
            enc_msg = cipher.msg_encrypt(secret_string)
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            dct_img_encoded = DCT.DCTEncoder(img, enc_msg, channelchoose())
            cv2.imwrite(outFile, dct_img_encoded)    
            displayImage("result/result.png")
    
        else:
            key = sp.get()
            try:
                cipher2 = AESCipher(key.encode())
                img4 = cv2.imread(outFile, cv2.IMREAD_UNCHANGED)
                DCT = DiscreteCosineTransform(image_path)
                msgbits = DCT.DCTDecoder(img4)
                a = msgbits.index(42)
                decoded = bytes(msgbits[a+1:])
                displaySecret(cipher2.msg_decrypt(decoded))
                #saveSecretToFile(cipher2.msg_decrypt(decoded))
            except:
                displaySecret("")
                tk.messagebox.showwarning('\nFalied To Extract The Message.\n','\nMaybe the key is incorrect!\n')
'''
def saveSecretToFile(secret):
    print("saveSecretToFile")
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(secret)
    f.write(text2save)
    f.close()
'''

def displayImage(path):
    print(type(path))
    # im = Image.fromarray(image)
    global processed_image_label
    # processed_image = ImageTk.PhotoImage(image=im)
    # print(type(processed_image))
    load = Image.open(path)
    processed_image = ImageTk.PhotoImage(load)
    processed_image_label.config(image=processed_image)
    processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def displaySecret(secret):
    clear_processed_image()
    global processed_image_label
    processed_image_label.config(text=secret)
    # processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def clear_processed_image():
    print("clear image")
    processed_image_label.config(image='')
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def channelchoose():
    sin = channel_clicked.get()
    if(sin == "channel = 1"):
        return 1
    elif(sin == "channel = 2"):
        return 2
    elif(sin == "channel = 3"):
        return 3


    

def technique_callback(*args):

    option = technique_options_clicked.get()
    print("technique_callback: ", option)
    data = ""
    if (option == technique_options[0]):
               data = "DCT"
    elif (option == technique_options[1]):
        data = "first_DCT "
    elif (option == technique_options[2]):
        data = "AES_DCT "
    print(data)

root = tk.Tk()
root.geometry("600x400")
root.title("Image Steganography")

top = tk.Frame(root, borderwidth=1,relief="solid")
top1 = tk.Frame(root, borderwidth=1,relief="solid")
bottom = tk.Frame(root, borderwidth=1,relief="solid")
left = tk.Frame(root, borderwidth=1, relief="solid")
right = tk.Frame(root, borderwidth=1, relief="solid")
container1 = tk.Frame(left, borderwidth=1, relief="solid")
container2 = tk.Frame(left, borderwidth=1, relief="solid")
container3 = tk.Frame(right, borderwidth=1, relief="solid")
container4 = tk.Frame(right, borderwidth=1, relief="solid")
container5 = tk.Frame(top, borderwidth=1, relief="solid")
key_label = tk.Label(container5, text="Must enter 16 bytes key!!!(only in AES_DCT)")
secret_label = tk.Label(container1, text="Enter secret")
# original_img_label = tk.Label(container2, text="Original Image")
#description_label = tk.Label(container3, text="Description")
# processed_img_label = tk.Label(container4, text="Processed Image")

top.pack(side="top", expand=False, fill="both")
top1.pack(side="top", expand=False, fill="both")
bottom.pack(side="bottom", expand=False, fill="both")
left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container1.pack(expand=False, fill="both", padx=5, pady=5)
container2.pack(expand=False, fill="both", padx=5, pady=5)
container3.pack(expand=False, fill="both", padx=5, pady=5)
container4.pack(expand=False, fill="both", padx=5, pady=5)
container5.pack(expand=False, fill="both", padx=5, pady=10)
container2wt = container2.winfo_width()

original_image_label = tk.Label(root, width=container2wt)
processed_image_label = tk.Label(root, width=container2wt)
key_label.pack()
secret_label.pack()
# original_img_label.pack()
#description_label.pack()
# processed_img_label.pack()


# Buttons
select_img_btn = tk.Button(root,text='Select Image', width=35, command=select_image)
select_img_btn.pack(in_=top, side="left")

select_secret_img_btn = tk.Button(root,text='Select secret file', width=35, command=select_secret_file)
select_secret_img_btn.pack(in_=top1, side="left")

clear_btn = tk.Button(root,text='Clear Image', width=35, command=clear_image)
clear_btn.pack(in_=bottom, side="left")

exit_btn = tk.Button(root,text='Exit App', width=35, command=exit_app)
exit_btn.pack(in_=bottom, side="right")

process_btn = tk.Button(root,text='Process', width=35, command=process)
process_btn.pack(in_=top1, side="right")

# Drop down menu
options = [
    "Encrypt",
    "Decrypt"
]
technique_options = [
    "DCT Algorithm - Default",
    "first_RGB_DCT",
    "AES_DCT"
]
channels = [
    "channel = 1",
    "channel = 2",
    "channel = 3",
]
options_clicked = tk.StringVar()
options_clicked.set(options[0])
technique_options_clicked = tk.StringVar()
technique_options_clicked.trace("w",technique_callback)
technique_options_clicked.set(technique_options[0])

channel_clicked = tk.StringVar()
channel_clicked.set(channels[0])

sp = tk.StringVar()
key = tk.Entry( width=250, textvariable=sp)
key.pack(in_=container5, anchor="n", side="right")


cdrop = tk.OptionMenu(root, channel_clicked, *channels)
cdrop.pack(in_=top, anchor="n", side="bottom")
drop = tk.OptionMenu(root, options_clicked, *options)
drop.pack(in_=top, anchor="n", side="bottom")
technique_drop = tk.OptionMenu(root, technique_options_clicked, *technique_options)
technique_drop.pack(in_=top1, anchor="n", side="bottom")

# textbox and scrollbar
text1 = tk.Text(root, width=35, height=5)
#text2 = tk.Text(root, width=35, height=5)
scrollbar1 = tk.Scrollbar(root)
#scrollbar2 = tk.Scrollbar(root)
scrollbar1.config(command=text1.yview)
#scrollbar2.config(command=text2.yview)
text1.config(yscrollcommand=scrollbar1.set)
#text2.config(yscrollcommand=scrollbar2.set)
scrollbar1.pack(in_=container1, side=tk.RIGHT, fill=tk.Y)
#scrollbar2.pack(in_=container3, side=tk.RIGHT, fill=tk.Y)
text1.pack(in_=container1, side=tk.LEFT, fill=tk.BOTH, expand=True)
#text2.pack(in_=container3, side=tk.LEFT, fill=tk.BOTH, expand=True)



root.mainloop()