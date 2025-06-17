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
    $job_number = trim($_POST['job_number'] ?? '');
    $customer = trim($_POST['customer'] ?? '');
    $jobsite_address = trim($_POST['jobsite_address'] ?? '');
    $drawing_desc = trim($_POST['drawing_desc'] ?? '');
    $status = trim($_POST['status'] ?? 'Pending');
    $notes = trim($_POST['notes'] ?? '');
    $title = trim($_POST['title'] ?? '');

    $filename = null;
    if (!empty($_FILES['file']['name'])) {
        $upload_dir = __DIR__ . '/uploads/';
        if (!is_dir($upload_dir)) {
            mkdir($upload_dir, 0777, true);
        }
        $basename = basename($_FILES['file']['name']);
        $target = $upload_dir . time() . '_' . preg_replace('/[^A-Za-z0-9._-]/', '_', $basename);
        if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
            $filename = basename($target);
        } else {
            $error = 'File upload failed';
        }
    }

    if ($error === '') {
        $stmt = $mysqli->prepare('INSERT INTO shop_drawing_requests (job_number, customer, jobsite_address, drawing_desc, filename, status, notes, title) VALUES (?,?,?,?,?,?,?,?)');
        if ($stmt) {
            $stmt->bind_param('ssssssss', $job_number, $customer, $jobsite_address, $drawing_desc, $filename, $status, $notes, $title);
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
    <title>Shop Drawing Request</title>
</head>
<body>
    <h1>Shop Drawing Request</h1>
    <?php if ($success): ?>
        <p style="color:green;">Request submitted successfully.</p>
    <?php elseif ($error !== ''): ?>
        <p style="color:red;"><?php echo htmlspecialchars($error); ?></p>
    <?php endif; ?>
    <form method="post" action="" enctype="multipart/form-data">
        <label>Job Number: <input type="text" name="job_number" required></label><br>
        <label>Customer: <input type="text" name="customer" required></label><br>
        <label>Jobsite Address:<br><textarea name="jobsite_address" rows="3" cols="40"></textarea></label><br>
        <label>Title: <input type="text" name="title"></label><br>
        <label>Drawing Description:
            <select name="drawing_desc">
                <option value="Plan">Plan</option>
                <option value="Section">Section</option>
                <option value="Detail">Detail</option>
                <option value="Elevation">Elevation</option>
                <option value="Other">Other</option>
            </select>
        </label><br>
        <label>File Attachment: <input type="file" name="file"></label><br>
        <label>Status:
            <select name="status">
                <option value="Pending">Pending</option>
                <option value="In Review">In Review</option>
                <option value="Completed">Completed</option>
            </select>
        </label><br>
        <label>Notes:<br><textarea name="notes" rows="4" cols="40"></textarea></label><br>
        <input type="submit" value="Submit Request">
    </form>
    <p><a href="drawing_requests.php">View Requests</a></p>
    <p><a href="index.php">Back to Dashboard</a></p>
</body>
</html>
