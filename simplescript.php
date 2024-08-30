<?php

// email address to send the form to
$to = 'mike@mbmotorcycletraining.co.uk';

// webpage to redirect to on success (relative to this script)
$success = 'success.htm';

// the fields to put in the email (corresponding to NAME of form inputs, 
// selects, textareas etc)
// Optionally use   =>   to rename a field when it appears in the email
$fields = array('name',
                'email',
                'telephone',
                'select' => 'Contact by',
                'Requirements');

// subject of email
$subject = 'Message received from Mike Barlow web form';

// email address and name the email will be from
$from = 'noreply@mbmotorcycletraining.co.uk';
$from_name = 'Mike Barlow';

/*****************************************************************************/

// Check that a valid email address was provided
if(!preg_match('/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i', $_POST['email'])) {
  die("Please provide a valid email address.");
}

// Set the reply-to field to the provided email address
$replyto = $_POST['email'];

// Compose email body
$message = "Message received from $from_name web form.";

// Use GMT timezone
date_default_timezone_set('Europe/London');
// Add date to email message
$message .= "\nSent on ".date('j M Y H:i T')."\n";

// Add the fields and their values
foreach ($fields as $field => $field_name) {
  $message .= "
".$field_name.": ".$_POST[(is_int($field)?$field_name:$field)];
}

// End of email body
$message .= "";

// Lines cannot be longer than 70 characters in emails
$message = wordwrap($message, 70);

// Set some headers
$headers = "From: $from_name <".$from.">\r\n"
          .'Reply-To: '.$_POST['email']."\r\n"
          .'X-Mailer: PHP/'.phpversion();

// Send the email
if(mail($to, $subject, $message, $headers)) {
  // Redirect to success page
  header('Location: '.$success);
} else {
  die('Email could not be sent, please email us manually.');
}


?>