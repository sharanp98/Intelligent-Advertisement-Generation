with open('reqd_images.txt', 'r') as f:
    reqd_images = f.read().splitlines()
print(reqd_images)
offer = reqd_images[-1]
print(offer)