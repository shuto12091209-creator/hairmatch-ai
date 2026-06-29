import cv2
import os

image_path = os.path.join("app", "uploads", "IMG_8678.png")

image = cv2.imread(image_path)

if image is None:
    print("画像を読み込めませんでした")
    print(f"確認したパス: {image_path}")
else:
    height, width, channels = image.shape

    print("画像の読み込みに成功しました！")
    print(f"横幅: {width}px")
    print(f"高さ: {height}px")
    print(f"チャンネル数: {channels}")