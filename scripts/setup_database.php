<?php
$host = getenv('DB_HOST') ?: 'localhost';
$user = getenv('DB_USER') ?: 'forgecore';
$pass = getenv('DB_PASSWORD') ?: 'forgecore';
$db   = getenv('DB_NAME') ?: 'forgecore';

$mysqli = new mysqli($host, $user, $pass);
if ($mysqli->connect_errno) {
    fwrite(STDERR, "Connection failed: {$mysqli->connect_error}\n");
    exit(1);
}

if (!$mysqli->query("CREATE DATABASE IF NOT EXISTS `$db`")) {
    fwrite(STDERR, "Database creation failed: {$mysqli->error}\n");
    exit(1);
}
$mysqli->select_db($db);

$schema = file_get_contents(__DIR__ . '/../database/schema.sql');
if ($schema === false) {
    fwrite(STDERR, "Could not read schema file\n");
    exit(1);
}

if ($mysqli->multi_query($schema)) {
    do {
        if ($result = $mysqli->store_result()) {
            $result->free();
        }
    } while ($mysqli->more_results() && $mysqli->next_result());
    echo "Database setup complete\n";
} else {
    fwrite(STDERR, "Error executing schema: {$mysqli->error}\n");
    exit(1);
}
$mysqli->close();
?>
