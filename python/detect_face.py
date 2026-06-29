import os
import sys
import cv2
import mediapipe as mp
import json


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

    # 顔の縦幅・横幅を計算
    face_height = abs(chin.y - forehead.y)
    face_width = abs(right_cheek.x - left_cheek.x)

    # 横幅が0の場合のエラー対策
    if face_width == 0:
        return {
            "success": False,
            "message": "顔の横幅を計算できませんでした"
        }

    # 縦横比を計算
    face_ratio = face_height / face_width

    # 顔型判定
    if face_ratio >= 1.45:
        face_shape = "面長"
    elif face_ratio <= 1.25:
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