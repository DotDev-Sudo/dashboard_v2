<?php
session_start(); // Start the session

// Create (or open) the SQLite database
$db = new SQLite3('database.db');

// Create users table if it does not exist
$db->exec("CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    emailID TEXT UNIQUE,
    password TEXT
)");

// Insert default admin user if it does not exist
$default_username = 'Admin';
$default_email = 'admin@dashboard.local';
$default_password = 'Password@123';
$hashed_password = password_hash($default_password, PASSWORD_BCRYPT);

$check_admin = $db->querySingle("SELECT COUNT(*) FROM users WHERE username = '$default_username'");

if ($check_admin == 0) {
    $stmt = $db->prepare("INSERT INTO users (username, emailID, password) VALUES (:username, :emailID, :password)");
    $stmt->bindValue(':username', $default_username, SQLITE3_TEXT);
    $stmt->bindValue(':emailID', $default_email, SQLITE3_TEXT);
    $stmt->bindValue(':password', $hashed_password, SQLITE3_TEXT);
    $stmt->execute();
}

// Handle login request
$error = "";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $stmt = $db->prepare("SELECT userid, password FROM users WHERE username = :username");
    $stmt->bindValue(':username', $username, SQLITE3_TEXT);
    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['userid'] = $user['userid'];
        $_SESSION['username'] = $username;
        header("Location: manage.html"); // Redirect to the dashboard
        exit;
    } else {
        $error = "Invalid username or password";
    }
}
?>
