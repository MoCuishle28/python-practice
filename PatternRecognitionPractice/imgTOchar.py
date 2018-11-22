from PIL import Image

_ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


#将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(_ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0+1)/length
    return _ascii_char[int(gray/unit)]


if __name__ == '__main__':
    im = Image.open('wm.png','r')
    h = im.size[0]
    w = im.size[1]
    im = im.resize((w,h),Image.NEAREST)

    txt = ""
    for i in range(h):
        for j in range(w):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)

   #字符画输出到文件
    with open("output.txt",'w') as f:
        f.write(txt)