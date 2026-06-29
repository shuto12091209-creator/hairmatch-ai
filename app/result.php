<?php include __DIR__ . "/includes/header.php"; ?>

<h1>診断結果</h1>

<?php
// 画像が送信されているか確認
if (!isset($_FILES["face_image"])) {
    echo "<p>画像が送信されていません。</p>";
    echo '<a href="upload.php">戻る</a>';
    include __DIR__ . "/includes/footer.php";
    exit;
}

$file = $_FILES["face_image"];

// アップロードエラー確認
if ($file["error"] !== UPLOAD_ERR_OK) {
    echo "<p>画像のアップロードに失敗しました。</p>";
    echo '<a href="upload.php">戻る</a>';
    include __DIR__ . "/includes/footer.php";
    exit;
}

// 保存先フォルダ
$uploadDir = __DIR__ . "/uploads/";

// uploadsフォルダがなければ作成
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// 拡張子を取得
$extension = strtolower(pathinfo($file["name"], PATHINFO_EXTENSION));

// ファイル名をユニークにする
$fileName = date("YmdHis") . "_" . bin2hex(random_bytes(4)) . "." . $extension;

// PHP側の保存パス
$savePath = $uploadDir . $fileName;

// ブラウザ表示用のパス
$imageUrl = "uploads/" . $fileName;

// Docker内でPythonに渡す画像パス
$dockerImagePath = "/var/www/html/uploads/" . $fileName;

// 画像を保存
if (!move_uploaded_file($file["tmp_name"], $savePath)) {
    echo "<p>画像の保存に失敗しました。</p>";
    echo '<a href="upload.php">戻る</a>';
    include __DIR__ . "/includes/footer.php";
    exit;
}

// Pythonを実行
$pythonPath = "/opt/venv/bin/python";
$scriptPath = "/var/www/python/detect_face.py";

$command = $pythonPath . " " . $scriptPath . " " . escapeshellarg($dockerImagePath);
$pythonOutput = shell_exec($command);

// JSONをPHPで扱える形に変換
$result = json_decode($pythonOutput, true);
?>

<h2>アップロード画像</h2>

<img
    src="<?php echo htmlspecialchars($imageUrl, ENT_QUOTES, "UTF-8"); ?>"
    alt="アップロード画像"
    style="max-width: 300px;"
>

<?php if (!$result): ?>

    <p>診断結果の読み取りに失敗しました。</p>
    <pre><?php echo htmlspecialchars($pythonOutput ?? "", ENT_QUOTES, "UTF-8"); ?></pre>

<?php elseif (!$result["success"]): ?>

    <p><?php echo htmlspecialchars($result["message"], ENT_QUOTES, "UTF-8"); ?></p>

<?php else: ?>

    <h2>あなたの顔型</h2>
    <p><?php echo htmlspecialchars($result["face_shape"], ENT_QUOTES, "UTF-8"); ?></p>

    <h2>顔の縦横比</h2>
    <p><?php echo htmlspecialchars($result["face_ratio"], ENT_QUOTES, "UTF-8"); ?></p>

    <?php if (isset($result["face_height"]) && isset($result["face_width"])): ?>
        <h2>計測データ</h2>
        <p>顔の縦幅：<?php echo htmlspecialchars($result["face_height"], ENT_QUOTES, "UTF-8"); ?></p>
        <p>顔の横幅：<?php echo htmlspecialchars($result["face_width"], ENT_QUOTES, "UTF-8"); ?></p>
    <?php endif; ?>

    <h2>おすすめ髪型</h2>
    <ul>
        <?php foreach ($result["recommendations"] as $hairstyle): ?>
            <li><?php echo htmlspecialchars($hairstyle, ENT_QUOTES, "UTF-8"); ?></li>
        <?php endforeach; ?>
    </ul>

<?php endif; ?>

<a href="upload.php">もう一度診断する</a>

<script>
window.addEventListener("beforeunload", function () {
    const imageName = <?php echo json_encode($fileName, JSON_UNESCAPED_UNICODE); ?>;

    const data = new FormData();
    data.append("image", imageName);

    navigator.sendBeacon("delete_image.php", data);
});
</script>

<?php include __DIR__ . "/includes/footer.php"; ?>