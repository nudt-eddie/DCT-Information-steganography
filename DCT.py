import cv2
import numpy as np
import itertools

quant = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                  [12, 12, 14, 19, 26, 58, 60, 55],
                  [14, 13, 16, 24, 40, 57, 69, 56],
                  [14, 17, 22, 29, 51, 87, 80, 62],
                  [18, 22, 37, 56, 68, 109, 103, 77],
                  [24, 35, 55, 64, 81, 104, 113, 92],
                  [49, 64, 78, 87, 103, 121, 120, 101],
                  [72, 92, 95, 98, 112, 100, 103, 99]])
class DiscreteCosineTransform():
    # created the constructor
    def __init__(self,imPath):
        self.message = None
        self.numBits = 0
        self.imPath = imPath

    # utility and helper function for DCT Based Steganography
    # helper function to stich the image back together
    def chunks(self, l, n):
        m = int(n)
        for i in range(0, len(l), m):
            yield l[i:i+m]
            
    # function to add padding to make the function dividable by 8x8 blocks
    def addPadd(self, img, row, col):
        img = cv2.resize(img, (col+(8-col % 8), row+(8-row % 8)))
        return img

    # main part
    # encoding function
    # applying dct for encoding
    def DCTEncoder(self, img, secret, channel):
        try:
            self.message = str(len(secret)).encode() + b'*' + secret.encode()
        except:
            self.message = str(len(secret)).encode() + b'*' + secret
        # get the size of the image in pixels
        row, col = img.shape[:2]
        if((col/8)*(row/8) < len(secret)):
            print("Error: Message too large to encode in image")
            return False
        if row % 8 or col % 8:
            img = self.addPadd(img, row, col)
        row, col = img.shape[:2]
        # split image into BGR channels
        BImg, GImg, RImg = cv2.split(img)
        # message to be hid in Green channel so converted to type float32 for dct function
        GImg_np = np.float32(GImg)
        # breaking the image into 8x8 blocks
        imgBlocks = [np.round(GImg_np[j:j+8, i:i+8]-128) for (j, i)
                    in itertools.product(range(0, row, 8), range(0, col, 8))]
        # blocks are run through dct / apply dct to it
        dctBlocks = [np.round(cv2.dct(ib)) for ib in imgBlocks]
        # print('imgBlocks', imgBlocks[0])
        # print('dctBlocks', dctBlocks[0])
        # blocks are run through quantization table / obtaining quantized dct coefficients
        messIndex = 0
        letterIndex = 0
        print(self.message)
        for qb in dctBlocks:
            bit = (self.message[messIndex] >> (7-letterIndex)) & 1
            DC = qb[0][0]
            DC = (int(DC) & ~31) | (bit * 15)
            qb[0][0] = np.float32(DC)
            letterIndex += 1
            if letterIndex == 8:
                letterIndex = 0
                messIndex += 1
                if messIndex == len(self.message):
                    break
        # writing the stereo image
        # blocks run inversely through quantization table
        # blocks run through inverse DCT
        sImgBlocks = [cv2.idct(B)+128 for B in dctBlocks]
        # puts the new image back together
        new_GImg = []
        for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    new_GImg.extend(block[rowBlockNum])
        new_GImg = np.array(new_GImg).reshape(row, col)
        # converted from type float32
        new_GImg = np.uint8(new_GImg)
        if channel == 1 :
            return cv2.merge((BImg, new_GImg, RImg))
        if (channel == 2 or channel == 3):
            RImg_np = np.float32(RImg)
            imgBlocks = [np.round(RImg_np[j:j+8, i:i+8]-128) for (j, i)
                        in itertools.product(range(0, row, 8), range(0, col, 8))]
            dctBlocks = [np.round(cv2.dct(ib)) for ib in imgBlocks]
            messIndex = 0
            letterIndex = 0
            for qb in dctBlocks:
                bit = (self.message[messIndex] >> (7-letterIndex)) & 1
                DC = qb[0][0]
                DC = (int(DC) & ~31) | (bit * 15)
                qb[0][0] = np.float32(DC)
                letterIndex += 1
                if letterIndex == 8:
                    letterIndex = 0
                    messIndex += 1
                    if messIndex == len(self.message):
                        break
            sImgBlocks = [cv2.idct(B)+128 for B in dctBlocks]
            new_RImg = []
            for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
                for rowBlockNum in range(8):
                    for block in chunkRowBlocks:
                        new_RImg.extend(block[rowBlockNum])
            new_RImg = np.array(new_RImg).reshape(row, col)
            new_RImg = np.uint8(new_RImg)

            BImg_np = np.float32(BImg)
            imgBlocks = [np.round(BImg_np[j:j+8, i:i+8]-128) for (j, i)
                        in itertools.product(range(0, row, 8), range(0, col, 8))]
            dctBlocks = [np.round(cv2.dct(ib)) for ib in imgBlocks]
            messIndex = 0
            letterIndex = 0
            for qb in dctBlocks:
                bit = (self.message[messIndex] >> (7-letterIndex)) & 1
                DC = qb[0][0]
                DC = (int(DC) & ~31) | (bit * 15)
                qb[0][0] = np.float32(DC)
                letterIndex += 1
                if letterIndex == 8:
                    letterIndex = 0
                    messIndex += 1
                    if messIndex == len(self.message):
                        break
            sImgBlocks = [cv2.idct(B)+128 for B in dctBlocks]
            new_BImg = []
            for chunkRowBlocks in self.chunks(sImgBlocks, col/8):
                for rowBlockNum in range(8):
                    for block in chunkRowBlocks:
                        new_BImg.extend(block[rowBlockNum])
            new_BImg = np.array(new_BImg).reshape(row, col)
            new_BImg = np.uint8(new_BImg)
        if channel == 2:    
            return cv2.merge((BImg, new_GImg, new_RImg))
        if channel == 3:
            return cv2.merge((new_BImg, new_GImg, new_RImg))

    # decoding
    # apply dct for decoding
    def DCTDecoder(self, img):
        row, col = img.shape[:2]
        messSize = None
        messageBits = []
        buff = 0
        # split the image into RGB channels
        BImg, GImg, RImg = cv2.split(img)
        # message hid in saturation channel so converted to type float32 for dct function
        GImg_np = np.float32(GImg)
        # break into 8x8 blocks
        imgBlocks = [GImg_np[j:j+8, i:i+8] -
                     128 for (j, i) in itertools.product(range(0, row, 8), range(0, col, 8))]
        dctBlocks = [np.round(cv2.dct(ib)) for ib in imgBlocks]
        # the blocks are run through quantization table
        print('imgBlocks', imgBlocks[0])
        print('dctBlocks', dctBlocks[0])
        i = 0
        # message is extracted from LSB of DCT coefficients
        for qb in dctBlocks:
            if qb[0][0] > 0:
                DC = int((qb[0][0]+7)/16) & 1
            else:
                DC = int((qb[0][0]-7)/16) & 1
            # unpacking of bits of DCT
            buff += DC << (7-i)
            i += 1
            if i == 8:
                messageBits.append(buff)
                buff = 0
                i = 0
                if messageBits[-1] == 42 and not messSize:
                    try:
                        messSize = chr(messageBits[0])
                        for j in range(1, len(messageBits)-1):
                            messSize += chr(messageBits[j])
                        messSize = int(messSize)
                        print(messSize, 'a')
                    except:
                        print('b')
            if len(messageBits) - len(str(messSize)) - 1 == messSize:
                print("msgbits", messageBits)
                return messageBits
        return None
    def DCTEn0(self, secret, outIm, channel):
        # load image for processing
        img = self.loadImage()
        if img is None:
            print("Error: File not found!")
            return

        self.message = str(len(secret)) + '*' + secret
        self.bitMess = self.toBits()

        # get size of image in pixels
        row, col = img.shape[:2]
        self.oriRow, self.oriCol = row, col

        if ((col / 8) * (row / 8) < len(secret)):
            print("Error: Message too large to encode in image")
            return

        # make divisible by 8x8
        if row % 8 != 0 or col % 8 != 0:
            img = self.addPadd(img, row, col)

        row, col = img.shape[:2]

        # split image into RGB channels
        bImg, gImg, rImg = cv2.split(img)

        if (channel == 1):
        # message to be hid in blue channel so converted to type float32 for dct function
            bImg = np.float32(bImg)
            # print(bImg[0:8,0:8])
            # break into 8x8 blocks
            imgBlocks = [np.round(bImg[j:j + 8, i:i + 8] - 128) for (j, i) in itertools.product(range(0, row, 8),
                                                                                                range(0, col, 8))]
        elif  (channel == 2):
            gImg = np.float32(gImg)
            imgBlocks = [np.round(gImg[j:j + 8, i:i + 8] - 128) for (j, i) in itertools.product(range(0, row, 8),
                                                                               range(0, col, 8))]
        elif  (channel == 3):
            rImg = np.float32(rImg)
            imgBlocks = [np.round(rImg[j:j + 8, i:i + 8] - 128) for (j, i) in itertools.product(range(0, row, 8),
                                                                               range(0, col, 8))]
        # print(imgBlocks[1][0])
        # Blocks are run through DCT function
        dctBlocks = [np.round(cv2.dct(img_Block)) for img_Block in imgBlocks]

        # blocks then run through quantization table
        quantizedDCT = [np.round(dct_Block / quant) for dct_Block in dctBlocks]

        messIndex = 0
        letterIndex = 0

        for quantizedBlock in quantizedDCT:
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)
            DC = np.unpackbits(DC)
            # print(DC, end=' ')
            DC[7] = self.bitMess[messIndex][letterIndex]
            # print(DC,end= ' ')
            DC = np.packbits(DC)

            # print(DC)
            DC = np.float32(DC)
            DC = DC - 255
            quantizedBlock[0][0] = DC

            letterIndex = letterIndex + 1
            if letterIndex == 8:
                letterIndex = 0
                messIndex = messIndex + 1
                if messIndex == len(self.message):
                    break

        # print(quantizedDCT[1][0])

        # blocks run inversely through quantization table
        sImgBlocks = [quantizedBlock * quant + 128 for quantizedBlock in quantizedDCT]

        # blocks run through inverse DCT
        # sImgBlocks = [cv2.idct(B)+128 for B in quantizedDCT]

        # puts the new image back together
        sImg = []
        for chunkRowBlocks in self.chunks(sImgBlocks, col / 8):
            for rowBlockNum in range(8):
                for block in chunkRowBlocks:
                    sImg.extend(block[rowBlockNum])
        sImg = np.array(sImg).reshape(row, col)

        # converted from type float32
        sImg = np.uint8(sImg)
        if(channel == 1):
            sImg = cv2.merge((sImg, gImg, rImg))
            cv2.imwrite(outIm, sImg)
            return sImg
        elif(channel == 2):
            sImg = cv2.merge((bImg, sImg, rImg))
            cv2.imwrite(outIm, sImg)
            return sImg
        elif(channel == 3):
            sImg = cv2.merge((bImg, gImg, sImg))
            cv2.imwrite(outIm, sImg)
            return sImg

    def DCTDe(self):
        img = cv2.imread(self.imPath, cv2.IMREAD_UNCHANGED)

        row, col = img.shape[:2]

        messSize = None
        messageBits = []
        buff = 0

        # split image into RGB channels
        bImg, gImg, rImg = cv2.split(img)
        # print(bImg[0:8,0:8])
        # message hid in blue channel so converted to type float32 for dct function
        bImg = np.float32(bImg)
        # print(bImg[0:8,0:8])

        # break into 8x8 blocks
        imgBlocks = [bImg[j:j + 8, i:i + 8] - 128 for (j, i) in itertools.product(range(0, row, 8),
                                                                                  range(0, col, 8))]
        # blocks run through quantization table
        # quantizedDCT = [dct_Block/ (quant) for dct_Block in dctBlocks]
        quantizedDCT = [img_Block / quant for img_Block in imgBlocks]
        # print(quantizedDCT[1][0])
        i = 0
        # message extracted
        for quantizedBlock in quantizedDCT:
            DC = quantizedBlock[0][0]
            DC = np.uint8(DC)
            DC = np.unpackbits(DC)
            if DC[7] == 1:
                buff += (0 & 1) << (7 - i)
            elif DC[7] == 0:
                buff += (1 & 1) << (7 - i)
            i = 1 + i
            if i == 8:

                messageBits.append(chr(buff))
                buff = 0
                i = 0

                if messageBits[-1] == '*' and messSize is None:
                    try:
                        messSize = int(''.join(messageBits[:-1]))
                    except:
                        pass
            if len(messageBits) - len(str(messSize)) - 1 == messSize:
                return ''.join(messageBits)[len(str(messSize)) + 1:]

        return ''
    def loadImage(self):
        # load image
        img = cv2.imread(self.imPath, cv2.IMREAD_UNCHANGED)

        if img is None:
            return None

        return img
    def toBits(self):
        bits = []

        for char in self.message:
            binval = bin(ord(char))[2:].rjust(8, '0')

            # for bit in binval:
            bits.append(binval)

        self.numBits = bin(len(bits))[2:].rjust(8, '0')
        return bits