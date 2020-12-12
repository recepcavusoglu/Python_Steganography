from PIL import Image
import PIL
from cryptography.fernet import Fernet
from scipy.io.wavfile import read,write
import numpy
from scipy import signal


class Steganography():
    def __init__(self,p_path):
        self.Path = p_path
    
    def Write_Audio(self,p_msg):
        a = read(self.Path)
        rate = a[0]
        data=numpy.array(a[1])
        my_Data = self.Char_ToBinary(p_msg)
        newdata = []
        loop1 = 0
        #Crate the data to write
        while (loop1<len(my_Data)):
            loop2 =0
            while(loop2<8):
                newdata.append(my_Data[loop1][loop2])
                loop2 +=1
            loop1 +=1
        #Message Lenght to Binary
        lenght = []
        dummy=len(p_msg)
        for i in range(32):
            if(dummy%2==0):
                lenght.insert(0,0)
                dummy=dummy>>1
            else:
                lenght.insert(0,1)
                dummy=dummy>>1
        #Write Data
        for i in range(len(newdata)):        
            if(newdata[i]==0):
                data[i][0] = data[i][0] >>1
                data[i][0] = data[i][0] <<1
            else:
                data[i][0] = data[i][0] | 1
        #Write Lenght
        for i in range(32):
            if(lenght[i]==0):
                data[i][1] = data[i][1] >>1
                data[i][1] = data[i][1] <<1
            else:
                data[i][1] = data[i][1] | 1
        write("Steganography.wav",rate,data)
        self.Path="Steganography.wav"

    def Read_Audio(self,p_path):
        audio = read(p_path)
        data=numpy.array(audio[1])
        size = 0
        #Get Message Lenght
        for i in range(32):
            size += ( data[i][1] & 1)*(2**(32-i-1))
        dummy=0
        count = 0    
        msg ="" 
        #Get Message
        for i in range(size*8):
            dummy += (data[i][0] &1)*(2**count)
            count +=1        
            if (count%8==0):
                msg += chr(dummy)
                dummy=0            
                count=0
        return msg
    
    #FUNCTION THAT ENCRYPTS THE MESSAGE RETURNS KEY TO DECRYPT AND ENCRYPTED MESSAGE
    def Encrypt(self,p_text):
        message= p_text.encode()
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return key, encrypted
    #FUNCTION THAT DECRYPTS THE MESSAGE
    def Decrypt(self,p_key,p_txt):
        f = Fernet(p_key)
        decrypted = f.decrypt(bytes(p_txt,'utf-8'))
        return decrypted.decode("utf-8")        
    #WRITES THE ENCRYPYTION KEY TO IMAGE'S BOTTOM RIGHT
    def Write_Key(self,p_key):
        array1 = bytearray(p_key, 'utf-8')
        charlist=list(array1)
        binarykey=[]
        for i in charlist:
            j=0
            dummylist=[]
            dummy = i
            while(j<8):         
                dummylist.append(dummy & 1)
                dummy = dummy>>1
                j+=1
            binarykey.append(dummylist)    
        im = Image.open(self.Path)
        pix = im.load()
        x=0
        y=0
        while(y<len(binarykey)):
            x=0
            while(x<8):
                r,g,b = pix[im.size[0]-x-1,im.size[1]-y-1]
                dum = binarykey[y][x]
                abc= dum & 1
                if(abc==0):
                    r = r>>1
                    r = r<<1
                else:
                    r = r| 1
                new_tuple = (r,g,b)
                pix[im.size[0]-x-1,im.size[1]-y-1] = new_tuple
                x+=1
            y+=1
        im.save("Steganography.bmp")
        self.Path="Steganography.bmp"
    #GETS THE ENCRYPTION KEY FROM IMAGE
    def Get_Key(self,p_encypath):
        im = Image.open(p_encypath)
        pix = im.load()
        i=0
        mykey=""
        while(i<44):
            j=0
            num=0
            while(j<8):
                x= im.size[0]-1-j
                y= im.size[1]-1-i
                num+=(pix[x,y][0]&1)*(2**j)
                j+=1
            mykey +=chr(num)
            i+=1
        return mykey
    #-----------
    #GETS THE MESSAGE LENGHT FROM IMAGE
    def Count(self,p_encypath):
        im = Image.open(p_encypath)
        pix = im.load()
        exp=0
        size = 0
        while(exp<32):
            size += (pix[0,exp][1] & 1)* (2**exp)
            exp+=1
        return size
    #-------------
    '''Char_ToBinary Fonksiyonunda oluşturduğumuz değerleri resmin pixellerindeki red değerlerinin 
    en düşük bitine yazıyoruz(8 bit olarak). green değerlerinde de aynı şekilde mesaj uzunluğu saklanır(32 bit olarak)'''

    #WRITES THE DATA THAT WE CREATE AT Char_ToBinary Function AT IMAGES LEAST SIGNIFICANT RED BIT.
    #ALSO WRITES MESSAGE LENGHT AT LEAST SIGNIFICANT GREEN BIT
    def Write_Binary(self,p_list,p_path):
        im = Image.open(p_path)
        pix = im.load()
        lenght = []
        x=0
        len_list = len(p_list)
        while(x<32):
            lenght.append(len_list & 1)
            len_list= len_list>>1  
            r,g,b = pix[0,x]
            if(lenght[x]==0):
                g= g>>1
                g= g<<1
            else:
                g = g| lenght[x]
            new_tuple = (r,g,b)
            pix[0,x] = new_tuple
            x+=1
        j=0
        i=0
        dumm_list=[]
        while(i<len(p_list)):
            while(j<8):           
                abc = p_list[i][j]
                r,g,b = pix[i,j]
                if(abc == 0):
                    r= r>>1 
                    r= r<<1 
                else:
                    r = r | abc
                dumm_list.append(r)
                new_tuple = (r,g,b)
                pix[i,j] = new_tuple
                j +=1
            j=0
            i +=1
        im.save("Steganography.bmp") 
    #-------------

    #-------------
    ''' RETURNS MESSAGE AS BINARY(BINARY ARRAY IS REVERSED FOR EASY READING) EXP : 
        abc ----->[[1, 0, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 1, 0]]  '''
    
    def Char_ToBinary(self,p_message):
        array1 = bytearray(p_message, 'utf-8')
        charlist=list(array1)
        binarylist=[]
        for i in charlist:
            j=0
            dummylist=[]
            dummy = i
            while(j<8):         
                dummylist.append(dummy & 1)
                dummy = dummy>>1
                j+=1
            binarylist.append(dummylist)
        return binarylist
    #-------------
    #READS BINARY VALUE FROM IMAGE AND RETURNS THE MESSAGE
    def Read(self,p_size,p_encypath):
        im = Image.open(p_encypath)
        pix = im.load()
        i=0
        mytext=""
        while(i<p_size):
            j=0
            num=0
            while(j<8):
                num+=(pix[i,j][0]&1)*(2**j)
                j+=1
            mytext +=chr(num)
            i+=1
        return mytext
        
    #---------------------

    def Write_Image(self,p_text):
        key , en = self.Encrypt(p_text)
        self.Write_Key(key.decode("utf-8"))
        self.Write_Binary(self.Char_ToBinary(en.decode("utf-8")),self.Path)

    def Read_Image(self,p_path):
        mykey = self.Get_Key(p_path)
        msg= self.Read(self.Count(p_path),p_path)
        return self.Decrypt(mykey,msg)

