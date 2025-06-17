<?php
$host = getenv('DB_HOST') ?: 'localhost';
$user = getenv('DB_USER') ?: 'forgecore';
$pass = getenv('DB_PASSWORD') ?: '';
$db   = getenv('DB_NAME') ?: 'forgecore';

$mysqli = new mysqli($host, $user, $pass, $db);
if ($mysqli->connect_errno) {
    die('Connection failed: ' . $mysqli->connect_error);
}

$result = $mysqli->query('SELECT id, job_number, customer, jobsite_address, drawing_desc, filename, status, notes, title, created_at FROM shop_drawing_requests ORDER BY created_at DESC');
$rows = $result ? $result->fetch_all(MYSQLI_ASSOC) : [];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shop Drawing Requests</title>
    <style>
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 4px; }
    </style>
</head>
<body>
    <h1>Shop Drawing Requests</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Job Number</th>
            <th>Customer</th>
            <th>Jobsite Address</th>
            <th>Title</th>
            <th>Description</th>
            <th>File</th>
            <th>Status</th>
            <th>Notes</th>
            <th>Created</th>
        </tr>
        <?php foreach ($rows as $row): ?>
            <tr>
                <td><?php echo htmlspecialchars($row['id']); ?></td>
                <td><?php echo htmlspecialchars($row['job_number']); ?></td>
                <td><?php echo htmlspecialchars($row['customer']); ?></td>
                <td><?php echo nl2br(htmlspecialchars($row['jobsite_address'])); ?></td>
                <td><?php echo htmlspecialchars($row['title']); ?></td>
                <td><?php echo htmlspecialchars($row['drawing_desc']); ?></td>
                <td>
                    <?php if ($row['filename']): ?>
                        <a href="uploads/<?php echo urlencode($row['filename']); ?>">Download</a>
                    <?php endif; ?>
                </td>
                <td><?php echo htmlspecialchars($row['status']); ?></td>
                <td><?php echo nl2br(htmlspecialchars($row['notes'])); ?></td>
                <td><?php echo htmlspecialchars($row['created_at']); ?></td>
            </tr>
        <?php endforeach; ?>
    </table>
    <p><a href="shop_drawing_request_form.php">Submit New Request</a></p>
    <p><a href="index.php">Back to Dashboard</a></p>
</body>
</html>
