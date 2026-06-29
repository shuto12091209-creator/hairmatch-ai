<?php
include 'includes/header.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $uploadDir = 'uploads/';

    $fileName = basename($_FILES['face_image']['name']);

    $uploadFile = $uploadDir . $fileName;

    if (move_uploaded_file($_FILES['face_image']['tmp_name'], $uploadFile)) {

        echo "<h1>アップロード成功！</h1>";

        echo "<p>保存場所：" . htmlspecialchars($uploadFile) . "</p>";

        echo "<img src='$uploadFile' width='300'>";

    } else {

        echo "<h1>アップロード失敗</h1>";

    }

} else {

    echo "<h1>不正なアクセスです</h1>";

}

include 'includes/footer.php';