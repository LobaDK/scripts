<?php
$files = glob('./*.{jpg,jpeg,gif,png,webm,mov,mp3,ogg,mp4}', GLOB_BRACE);
$count = count($files);
$index = rand(0, ($count-1));
$filename = $files[$index];

$extension = pathinfo($filename, PATHINFO_EXTENSION);

if (in_array($extension, array('jpg','jpeg','gif','png')))
{
        echo "<img style=\"max-width: 100%; height: auto;\" src=\"$filename\" alt=\"$filename\">";
        echo "<br />";
        echo "<a href=\"$filename\"> Direct link </a>";
}
else if (in_array($extension, array('mp4','mov','webm')))
{
        echo "<video controls style=\"max-width: 100%; height: auto;\"> <source src=\"$filename\" alt=\"$filename\"></video>";
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
