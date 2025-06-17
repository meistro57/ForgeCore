<?php
$host = getenv('DB_HOST') ?: 'localhost';
$user = getenv('DB_USER') ?: 'forgecore';
$pass = getenv('DB_PASSWORD') ?: '';
$db   = getenv('DB_NAME') ?: 'forgecore';

$mysqli = new mysqli($host, $user, $pass, $db);
if ($mysqli->connect_errno) {
    die('Connection failed: ' . $mysqli->connect_error);
}

$success = false;
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $address = trim($_POST['address'] ?? '');
    if ($name === '') {
        $error = 'Name is required';
    } else {
        $stmt = $mysqli->prepare('INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)');
        if ($stmt) {
            $stmt->bind_param('ssss', $name, $email, $phone, $address);
            if ($stmt->execute()) {
                $success = true;
            } else {
                $error = 'Insert failed: ' . $stmt->error;
            }
            $stmt->close();
        } else {
            $error = 'Prepare failed: ' . $mysqli->error;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add Customer</title>
</head>
<body>
    <h1>Add Customer</h1>
    <?php if ($success): ?>
        <p style="color:green;">Customer added successfully.</p>
    <?php elseif ($error !== ''): ?>
        <p style="color:red;"><?php echo htmlspecialchars($error); ?></p>
    <?php endif; ?>
    <form method="post" action="">
        <label>Name: <input type="text" name="name" required></label><br>
        <label>Email: <input type="email" name="email"></label><br>
        <label>Phone: <input type="text" name="phone"></label><br>
        <label>Address:<br><textarea name="address" rows="4" cols="40"></textarea></label><br>
        <input type="submit" value="Add Customer">
    </form>
    <p><a href="index.php">Back to Dashboard</a></p>
</body>
</html>
