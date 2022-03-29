from pathlib import Path
import json
import cv2
import matplotlib.pyplot as plt


def rectangle_prtint(path):
    stats_path = Path(path)
    file_last_name = stats_path.suffixes
    if file_last_name[0] != '.json':
        print('path trouble')
        assert False
    with open(stats_path, 'r') as f:
        x = json.load(f)
        for a in x: # 遍历boxes
            tmp = x[a]
            for i in tmp:  # 遍历name
                if i['name'] == 'box_b':
                    print(i['rectangle'])
                    l_t = i['rectangle']['left_top']
                    r_b = i['rectangle']['right_bottom']
    return l_t, r_b

def ratio_resize(img_path,target_size):
    image = cv2.imread(img_path)
    img_size = image.shape[:2]    # H, W

    # 取最小比率
    ratio = min(float(target_size[0]) / (img_size[0]), float(target_size[1]) / (img_size[1]))

    # 新size
    new_h = int(img_size[0] * ratio)
    new_w = int(img_size[1] * ratio)
    new_size = (new_h, new_w)

    new_img = cv2.resize(image, (new_size[1], new_size[0])) # W, H

    # 填充0
    pad_w = target_size[1] - new_size[1]
    pad_h = target_size[0] - new_size[0]
    top, bottom = pad_h//2, pad_h - (pad_h//2)
    left, right = pad_w//2, pad_w - (pad_w//2)
    img_new = cv2.copyMakeBorder(new_img, top, bottom, left, right, cv2.BORDER_CONSTANT, None, (0,0,0))
    return img_new
def normal_resize(img_path,target_size):
    image = cv2.imread(img_path)
    # img_size = image.shape[:2]    # H,W
    new_image = cv2.resize(image, (target_size[1], target_size[0]))
    return new_image

def cut_fill(orginal_image, stick_image, json_path, stick_mode=None):
    org_img = cv2.imread(orginal_image)

    left_top, right_bottom = rectangle_prtint(json_path)
    size = (right_bottom[1]-left_top[1], right_bottom[0]-left_top[0])

    if stick_mode == 'normal':
        stk_img = normal_resize(stick_image, size)
    elif stick_mode == 'ratio':
        stk_img = ratio_resize(stick_image, size)
        # print(stk_img.shape)
    else:
        print('mode false')
        assert False

    org_img[left_top[1]:right_bottom[1], left_top[0]:right_bottom[0], :] = stk_img[:, :, :]
    return org_img


# # 打印字段
# path_json = 'boxes.json'
# rectangle_prtint(path_json)

# # 填充
# path_json = 'boxes.json'
# img1 = 'image_1.jpg'
# img2 = 'image_2.jpg'
# im = cut_fill(img1, img2, path_json, stick_mode='ratio')
# plt.imshow(im)
# plt.show()

