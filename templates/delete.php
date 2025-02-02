<?php
// Security check to ensure only authorized files are deleted
if (isset($_GET['file'])) {
    // Single file deletion
    $file = $_GET['file'];
    $mediaDir = 'media/';

    if (file_exists($mediaDir . $file)) {
        if (unlink($mediaDir . $file)) {
            echo json_encode(['status' => 'success']);
        } else {
            echo json_encode(['status' => 'error']);
        }
    } else {
        echo json_encode(['status' => 'error']);
    }
} elseif (isset($_GET['files'])) {
    // Multiple files deletion
    $files = json_decode($_GET['files']);
    $mediaDir = 'media/';
    $success = true;

    foreach ($files as $file) {
        if (file_exists($mediaDir . $file)) {
            if (!unlink($mediaDir . $file)) {
                $success = false;
            }
        }
    }

    if ($success) {
        echo json_encode(['status' => 'success']);
    } else {
        echo json_encode(['status' => 'error']);
    }
} else {
    echo json_encode(['status' => 'error']);
}
?>
