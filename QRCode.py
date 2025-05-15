import qrcode

#URL that is encoded into my qr code
url = "http://10.1.1.20:5001/checkout" #local host url

#Generate the qrcode
qr = qrcode.QRCode(
    version = 1, #Size of the QR code
    error_correction=qrcode.constants.ERROR_CORRECT_L, #Error Correction
    box_size=10, #Size of each box in the QR code grid
    border= 4, #Thickness of the border around the QR code

)
qr.add_data(url) #Add the URL to the QR code
qr.make(fit=True)

#Create an image from the QR code
img = qr.make_image(fill= 'black', back_color= 'white')

#Save the Image to a file
img.save("GameWebsiteQRcode.png") #Saves the QR code as a .png file