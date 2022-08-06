<?php
$files = glob('./*.{jpg,jpeg,gif,png,webm,mov,mp3,ogg,mp4}', GLOB_BRACE);
$count = count($files);
$index = rand(0, ($count-1));
$filename = $files[$index];

echo($filename)
?>