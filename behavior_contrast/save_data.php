<?php
header('Content-Type: application/json');

// Create results directory if it doesn't exist
$resultsDir = 'results';
if (!file_exists($resultsDir)) {
    mkdir($resultsDir, 0777, true);
}

// Get the raw POST data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data || !isset($data['filename']) || !isset($data['data'])) {
    echo json_encode([
        'success' => false,
        'message' => "Invalid data received"
    ]);
    exit;
}

$filename = $data['filename'];
$experimentData = $data['data'];

// Sanitize filename
$filename = preg_replace('/[^a-zA-Z0-9\-_\.]/', '', $filename);
$filepath = $resultsDir . '/' . $filename;

try {
    // Save data to JSON file
    file_put_contents($filepath, json_encode($experimentData, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'success' => true,
        'message' => 'Data saved successfully'
    ]);
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => "Error: " . $e->getMessage()
    ]);
}
?>