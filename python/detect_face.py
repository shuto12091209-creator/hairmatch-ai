import os
import sys
import cv2
import mediapipe as mp
import json
import math


base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "face_landmarker.task")


def analyze_face(image_path):
    # 画像が読み込めるか確認
    image = cv2.imread(image_path)

    if image is None:
        return {
            "success": False,
            "message": "画像を読み込めませんでした",
            "path": image_path
        }

    # 画像サイズを取得
    image_height, image_width, _ = image.shape

    # モデルファイルがあるか確認
    if not os.path.exists(model_path):
        return {
            "success": False,
            "message": "モデルファイルが見つかりません",
            "path": model_path
        }

    # MediaPipe Tasks API の準備
    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1
    )

    # MediaPipe用に画像を読み込む
    mp_image = mp.Image.create_from_file(image_path)

    # 顔の特徴点を検出
    with FaceLandmarker.create_from_options(options) as landmarker:
        detection_result = landmarker.detect(mp_image)

    # 顔が検出できなかった場合
    if not detection_result.face_landmarks:
        return {
            "success": False,
            "message": "顔を検出できませんでした"
        }

    # 1人目の顔の特徴点を取得
    landmarks = detection_result.face_landmarks[0]

    # 顔型判定に使う特徴点
    forehead = landmarks[10]      # 額付近
    chin = landmarks[152]         # 顎
    left_cheek = landmarks[234]   # 左頬
    right_cheek = landmarks[454]  # 右頬

    # MediaPipeの0〜1座標をピクセル座標に変換
    def to_pixel(point):
        return {
            "x": point.x * image_width,
            "y": point.y * image_height
        }

    forehead_px = to_pixel(forehead)
    chin_px = to_pixel(chin)
    left_cheek_px = to_pixel(left_cheek)
    right_cheek_px = to_pixel(right_cheek)

    # 顔の縦幅・横幅をピクセル距離で計算
    face_height = math.sqrt(
        (chin_px["x"] - forehead_px["x"]) ** 2 +
        (chin_px["y"] - forehead_px["y"]) ** 2
    )

    face_width = math.sqrt(
        (right_cheek_px["x"] - left_cheek_px["x"]) ** 2 +
        (right_cheek_px["y"] - left_cheek_px["y"]) ** 2
    )

    # 横幅が0の場合のエラー対策
    if face_width == 0:
        return {
            "success": False,
            "message": "顔の横幅を計算できませんでした"
        }

    # 縦横比を計算
    face_ratio = face_height / face_width

    # 顔型判定
    FaceLength = 1.25
    FaceWidth = 1.15

    if face_ratio >= FaceLength:
        face_shape = "面長"
    elif face_ratio <= FaceWidth:
        face_shape = "丸顔"
    else:
        face_shape = "卵型"

    # 顔型ごとのおすすめ髪型
    recommendations_map = {
        "面長": ["センターパート", "アップバング", "ウルフ"],
        "丸顔": ["マッシュ", "ショート", "ツーブロック"],
        "卵型": ["ナチュラルショート", "センターパート", "韓国風マッシュ"]
    }

    # 結果を返す
    return {
        "success": True,
        "face_shape": face_shape,
        "face_ratio": round(face_ratio, 3),
        "face_height": round(face_height, 1),
        "face_width": round(face_width, 1),
        "recommendations": recommendations_map.get(face_shape, [])
    }


# コマンドで直接実行されたときの処理
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
    else:
        image_path = os.path.join("app", "uploads", "IMG_8678.png")

    result = analyze_face(image_path)
    print(json.dumps(result, ensure_ascii=False))