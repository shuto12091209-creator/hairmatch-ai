<?php include 'includes/header.php'; ?>

<h1>写真アップロード</h1>

<form action="result.php" method="POST" enctype="multipart/form-data">

    <label>顔写真を選択してください</label><br><br>

    <input type="file" name="face_image" accept="image/*" required>

    <br><br>

    <button type="submit">
        診断する
    </button>

</form>

<?php include 'includes/footer.php'; ?>