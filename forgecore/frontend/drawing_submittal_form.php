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
    $drawing_number = trim($_POST['drawing_number'] ?? '');
    $job_number = trim($_POST['job_number'] ?? '');
    $description = trim($_POST['description'] ?? '');
    $submitted_by = trim($_POST['submitted_by'] ?? '');
    $submission_date = trim($_POST['submission_date'] ?? '');
    $status = trim($_POST['status'] ?? 'Submitted');

    // Basic validation
    if ($drawing_number === '' || $job_number === '' || $submitted_by === '') {
        $error = 'Drawing number, job number and submitted by are required.';
    } elseif ($status !== 'Submitted' && $status !== 'Reviewed' && $status !== 'Approved') {
        $error = 'Invalid status value.';
    } else {
        if ($submission_date === '') {
            $submission_date = date('Y-m-d');
        }
        // Use prepared statement
        $stmt = $mysqli->prepare('INSERT INTO drawing_submittals (drawing_number, job_number, description, submitted_by, submission_date, status) VALUES (?, ?, ?, ?, ?, ?)');
        if ($stmt) {
            $stmt->bind_param('ssssss', $drawing_number, $job_number, $description, $submitted_by, $submission_date, $status);
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
    <title>Drawing Submittal</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container py-4">
    <h1>Drawing Submittal Form</h1>
    <?php if ($success): ?>
        <div class="alert alert-success">Drawing submitted successfully.</div>
    <?php elseif ($error !== ''): ?>
        <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>
    <form method="post" action="" class="mt-3">
        <div class="mb-3">
            <label class="form-label">Drawing Number</label>
            <input type="text" name="drawing_number" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Job Number</label>
            <input type="text" name="job_number" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea name="description" class="form-control" rows="3"></textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Submitted By</label>
            <input type="text" name="submitted_by" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Submission Date</label>
            <input type="date" name="submission_date" class="form-control">
        </div>
        <div class="mb-3">
            <label class="form-label">Status</label>
            <select name="status" class="form-select">
                <option value="Submitted">Submitted</option>
                <option value="Reviewed">Reviewed</option>
                <option value="Approved">Approved</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <p class="mt-3"><a href="index.php">Back to Dashboard</a></p>
</body>
</html>
