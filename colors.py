blue = (0, 0, 128)
black = (0,0,0)
white = (255,255,255)
shadow = (192, 192, 192)
white = (255, 255, 255)
lightGreen = (0, 255, 0)
green = (0, 200, 0)
darkGreen = (0, 100, 0)
yellow = (255,255,0)
blue = (0, 0, 128)
lightBlue = (0, 0, 255)
cyan = (50, 255, 255)
red = (200, 0, 0)
lightRed = (255, 100, 100)
purple = (102, 0, 102)
orangeRed = (255,69,0)


def dark(color, *args):
    try:
        col2 = list(color)
    except:
        print("Not valid color")
        return

    returnCol = []
    for val in col2:
        if val != 0:
            if args:
                returnCol.append(max(val-args[0], 0))
            else:
                returnCol.append(max(val/2, 0))
        else:
            returnCol.append(val)
    
    return tuple(returnCol)

def light(color, *args):
    try:
        col2 = list(color)
    except:
        print("Not valid color")
        return

    returnCol = []
    for val in col2:
        if args:
            returnCol.append(val+args[0])
        else:
            returnCol.append(val*2)

    return tuple(returnCol)

def rgba(rgb, alpha):
    return tuple([rgb[0], rgb[1], rgb[2], max(min(255, alpha), 0)])
