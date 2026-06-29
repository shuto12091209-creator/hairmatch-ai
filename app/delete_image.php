<?php

header("Content-Type: application/json; charset=UTF-8");

// POST以外は拒否
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode([
        "success" => false,
        "message" => "POSTのみ対応しています"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// image が送られているか確認
if (!isset($_POST["image"])) {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "画像名がありません"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// ファイル名だけを取り出す
$fileName = basename($_POST["image"]);

// uploads フォルダ
$uploadDir = __DIR__ . "/uploads/";
$filePath = $uploadDir . $fileName;

// 実際のパスを取得
$realUploadDir = realpath($uploadDir);
$realFilePath = realpath($filePath);

// 不正なパスを防ぐ
if ($realFilePath === false || strpos($realFilePath, $realUploadDir) !== 0) {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "不正なファイルです"
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// ファイルがあれば削除
if (file_exists($realFilePath)) {
    unlink($realFilePath);
}

echo json_encode([
    "success" => true,
    "message" => "画像を削除しました"
], JSON_UNESCAPED_UNICODE);