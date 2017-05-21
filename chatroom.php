<?php

session_start();
$_SESSION['username']=$_POST['username'];

?>


<html>

<head>
<title>Chat Room</title>
</head>

<FRAMESET cols="200, *">
	<FRAME src="sidebar.php">
	<FRAMESET rows="*, 200">
		<FRAME src="messages.php">
		<FRAME src="newmessage.php">
	</FRAMESET>	
</FRAMESET>

</html>





<?php

echo $_POST['username'];

?>