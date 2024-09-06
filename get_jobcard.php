<?php
header('Content-Type: text/html; charset=utf-8');

$type = $_GET['type'];
$input = $_GET['input'];

// Load XML file
$xml = simplexml_load_file('jobcards.xml');

// Search XML data
$result = '';
foreach ($xml->jobcard as $jobcard) {
    if ($jobcard->$type == $input) {
        $result .= '<h2>Jobcard Details</h2>';
        $result .= '<p><strong>Requisition Number:</strong> ' . $jobcard->requisition-number . '</p>';
        $result .= '<p><strong>Jobcard Number:</strong> ' . $jobcard->jobcard-number . '</p>';
        $result .= '<p><strong>Requested By:</strong> ' . $jobcard->requested-by . '</p>';
        $result .= '<p><strong>Date:</strong> ' . $jobcard->date . '</p>';
        $result .= '<p><strong>Time Start:</strong> ' . $jobcard->time-start . '</p>';
        $result .= '<p><strong>Time Stop:</strong> ' . $jobcard->time-stop . '</p>';
        $result .= '<p><strong>Fault Description:</strong> ' . $jobcard->fault-description . '</p>';
        $result .= '<p><strong>Department:</strong> ' . $jobcard->department . '</p>';
        $result .= '<p><strong>Machine:</strong> ' . $jobcard->machine . '</p>';
        $result .= '<p><strong>Work Carried Out:</strong> ' . $jobcard->work-carried-out . '</p>';
        $result .= '<p><strong>Type of Fault:</strong> ' . $jobcard->type-of-fault . '</p>';
        $result .= '<p><strong>Artisan:</strong> ' . $jobcard->artisan . '</p>';
        $result .= '<p><strong>Apprentice:</strong> ' . $jobcard->apprentice . '</p>';
        $result .= '<p><strong>Total Time:</strong> ' . $jobcard->total-time . '</p>';
        break; // Exit loop after finding the first match
    }
}

if (empty($result)) {
    $result = '<p>No matching jobcard found.</p>';
}

echo $result;
?>
