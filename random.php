<?php
$files = glob('./*.{jpg,jpeg,gif,png,webm,mov,mp3,mp4}', GLOB_BRACE);
$count = count($files);
$index = rand(0, ($count-1));
$filename = $files[$index];

$extension = pathinfo($filename, PATHINFO_EXTENSION);

if (in_array($extension, array('jpg','jpeg','gif','png')))
{
        echo "<img src=\"$filename\" alt=\"$filename\" style=\"max-width: 100%; max-height: 1000%; margin: auto;\">";
        echo "<br />";
        echo "<a href=\"$filename\"> Direct link </a>";
}
else if (in_array($extension, array('mp4','mov','webm')))
{
        echo "<video src=\"$filename\" alt=\"$filename\" controls style=\"max-width: 100%; max-height: 100%; margin: auto;\">";
        echo "<br />";
        echo "<a href=\"$filename\"> Direct link </a>";
}
else if (in_array($extension, array('mp3','ogg')))
{
        echo "<audio src=\"$filename\" alt=\"$filename\" controls>";
        echo "<br />";
        echo "<a href=\"$filename\"> Direct link </a>";
}
?>
