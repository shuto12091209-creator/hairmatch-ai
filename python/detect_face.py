import os
import cv2
import mediapipe as mp

image_path = os.path.join("app", "uploads", "IMG_8678.png")
model_path = os.path.join("python", "models", "face_landmarker.task")

image = cv2.imread(image_path)

if image is None:
    print("画像を読み込めませんでした")
    print(f"確認したパス: {image_path}")
    exit()

print("画像の読み込みに成功しました！")

if not os.path.exists(model_path):
    print("モデルファイルが見つかりません")
    print(f"確認したパス: {model_path}")
    exit()

print("モデルファイルを確認しました！")

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1
)

mp_image = mp.Image.create_from_file(image_path)

with FaceLandmarker.create_from_options(options) as landmarker:
    result = landmarker.detect(mp_image)

if not result.face_landmarks:
    print("顔を検出できませんでした")
else:
    landmarks = result.face_landmarks[0]

    print("顔を検出しました！")
    print(f"取得できた特徴点の数：{len(landmarks)}")

    chin = landmarks[152]
    print(f"顎の座標：x={chin.x}, y={chin.y}, z={chin.z}")
    
    # 顔型判定用の特徴点
forehead = landmarks[10]      # 額付近
chin = landmarks[152]         # 顎
left_cheek = landmarks[234]   # 左頬
right_cheek = landmarks[454]  # 右頬

# 顔の縦幅・横幅を計算
face_height = abs(chin.y - forehead.y)
face_width = abs(right_cheek.x - left_cheek.x)

# 縦横比
face_ratio = face_height / face_width

print(f"顔の縦幅：{face_height}")
print(f"顔の横幅：{face_width}")
print(f"顔の縦横比：{face_ratio}")

# 顔型判定
if face_ratio >= 1.45:
    face_shape = "面長"
elif face_ratio <= 1.25:
    face_shape = "丸顔"
else:
    face_shape = "卵型"

print(f"判定結果：{face_shape}")