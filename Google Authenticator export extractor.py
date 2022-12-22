from pyzbar.pyzbar import decode
from PIL import Image
import subprocess
import glob
import cv2
import qrcode

ii = 0
for file in glob.glob(r'C:\Users\nickl\Pictures\QR codes\*'):

    decodeQR = decode(Image.open(file))

    p = subprocess.Popen(['C:\self installed apps\otpauth-v0.5.0-windows-amd64\otpauth.exe', '-link', decodeQR[0].data.decode()], stdout=subprocess.PIPE)
    otp, _ = p.communicate()

    otp = otp.decode().split('\n')


    for i in range(len(otp)):
        if otp[i]:
            ii += 1
            otp_dict = dict(substring.split('=') for substring in otp[i].split('&'))
            if 'issuer' in otp_dict:
                issuer = otp_dict['issuer']
            else:
                print(otp[i])
                issuer = input('\nNo issuer detected. Please give one: ')
            img = qrcode.make(otp[i])
            img.save(f'{issuer} OTP QR {ii}.png')
            while True:
                cv2.imshow('QRCode', cv2.imread(f'{issuer} OTP QR.png'))
                if cv2.waitKey(1) == ord('q'):
                    break