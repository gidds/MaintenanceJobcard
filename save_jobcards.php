<?php

echo '<pre>';
print_r($_POST);
echo '</pre>';

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input data
    $fields = [
        'requisition-number', 'jobcard-number', 'requested-by', 'date',
        'time-start', 'time-stop', 'fault-description', 'department',
        'machine', 'work-carried-out', 'type-of-fault', 'artisan',
        'apprentice', 'total-time'
    ];

    $data = [];
    foreach ($fields as $field) {
        $data[$field] = isset($_POST[$field]) ? htmlspecialchars($_POST[$field]) : '';
    }

    // Default value for total-time if not set
    $data['total-time'] = $data['total-time'] ?: '0 hours 0 minutes';

    $xmlFileName = 'jobcards.xml';

    if (file_exists($xmlFileName)) {
        $xml = simplexml_load_file($xmlFileName);

        // Check if jobcard with the same requisition number and jobcard number already exists
        $existing = false;
        foreach ($xml->jobcard as $jobcard) {
            if ((string)$jobcard->{'requisition-number'} === $data['requisition-number'] &&
                (string)$jobcard->{'jobcard-number'} === $data['jobcard-number']) {
                // Update existing jobcard
                foreach ($data as $key => $value) {
                    $jobcard->{$key} = $value;
                }
                $existing = true;
                break;
            }
        }

        if (!$existing) {
            // Add new jobcard entry
            $jobcard = $xml->addChild('jobcard');
            foreach ($data as $key => $value) {
                $jobcard->addChild($key, $value);
            }
        }
    } else {
        // Create a new XML document if it doesn't exist
        $xml = new SimpleXMLElement('<jobcards/>');
        $jobcard = $xml->addChild('jobcard');
        foreach ($data as $key => $value) {
            $jobcard->addChild($key, $value);
        }
    }

    // Save XML to file
    $xml->asXML($xmlFileName);

    // Redirect to jobcards.html with success parameter
    header('Location: success.php');
    exit();
}
?>
