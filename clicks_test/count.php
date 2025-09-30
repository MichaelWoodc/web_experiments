<?php
// count.php
$file = 'count.txt';

// Initialize file if missing
if (!file_exists($file)) {
    file_put_contents($file, '0');
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Increment count atomically
    $fp = fopen($file, 'c+');
    if (flock($fp, LOCK_EX)) {
        $count = (int)fread($fp, filesize($file));
        if (!$count && filesize($file) == 0) $count = 0;
        $count++;
        ftruncate($fp, 0);
        rewind($fp);
        fwrite($fp, $count);
        fflush($fp);
        flock($fp, LOCK_UN);
        fclose($fp);
        echo json_encode(['count' => $count]);
        exit;
    }
    fclose($fp);
    http_response_code(500);
    echo json_encode(['error' => 'Could not lock file']);
    exit;
} else {
    // GET request: return current count
    $count = (int)file_get_contents($file);
    header('Content-Type: application/json');
    echo json_encode(['count' => $count]);
}
?>
