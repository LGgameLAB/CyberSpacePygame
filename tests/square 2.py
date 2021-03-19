def sq2(num):
    while num != 1:
        num = num/2
        if num < 1:
            return False

    return True

print(sq2(14))