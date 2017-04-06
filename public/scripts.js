
var isrunning = false;
var information = function (message, index) {
	if (index < message.length) {
		isrunning = true;
	 	$('#info').append(message[index++]);
		setTimeout(function () { information(message, index);}, 2);
		}
	else isrunning = false;
};
$(function(){
	$('#skillWeb').click(function(){
		if (isrunning == false){
		$('#info').text("");
		information("I know my fair share about website creation! I know how to work with html to organize the necessary tags in order to fufill the requirements of the website. I know how to insert images, videos, add click and drag functionality, and many other functions. I also know a lot of CSS and JavaScript. I've organized this particular page with a lot of CSS and some JavaScript functionality (well, specifically jQuerry). I am pretty good at forms too!", 0);
		}
		else{
		isrunning = false;
		}
		
	});
	});
	$(function(){
	$('#skillWindows').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("I'm fairly good at programming in C#. I know my way around LINQ, creating classes and instances of those classes, creating relavant fields for those objects, and putting it all to good use! I'm good at working with linked lists, too; however I prefer using databases when it gets to be like that! In class, I created a little banking application where you could create new accounts, deposit/withdrawl money, determine account time, gather required info(such as ID, address, etc.), and create bills to pay directly from the account. No real money was used during the process.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});
	$(function(){
	$('#skillServer').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("I have experience working with Microsoft SQL Server and Oracle Databases from the classes I took in college. I learned how to create a query to create, update, or drop tables. I also know how to use T-SQL. I can insert data into those tables, remove data from tables, and create audit trails in order to see the modification history of a table. I also learned how to work with MySQL and PostgreSQL in my spare time in college.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});
$(function(){
	$('#skillAndroid').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("My favorite thing that I learned in my degree was how to create Android Applications. I learned how to modify the Manifest file to add permissions, and modify information. I also learned how to work with on click listeners, modify the layout in XML as well as with the GUI, and work with SQLite Databases to keep data stored locally. I even created a ticket tracking application in class for helpdesk tickets. It's a lot of fun. In my free time, I'm learning more about using other functions of Android such as GPS, NFC, and the gyroscopes.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});
$(function(){
	$('#skillApple').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("In class, we mostly worked with Objective-C and Swift. We didn't get to work with X-Code due to not having Macs at the college. I still believe that with a little guidance, I will be able to create applications with X-Code. I have watched some Youtube videos on it so that I can be a little better prepared if I need to create applications for Apple devices.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});
$(function(){
	$('#skillGit').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("In my free time, I've done some learning on GIT. We didn't learn this in class; however, it seems pretty easy to work with. I can initialize git, add all files to the location, push it, and pull it. I can also add messages to comment what changes have been made. I also know how to obtain an SSH certificate and push to a remote server such as Heroku.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});
$(function(){
	$('#skillROR').click(function(){
		if (isrunning == false){
			isrunning == true;
			$('#info').text("");
		information("Ruby on Rails is one of the more fun things I've worked on. I followed a free Udemy cource on the creation of a Rails server, as well as working with Ruby. I really enjoyed it as it helped shine a little light on how blogs are run.", 0);
		}
		else{
			isrunning = false;
		}
		});
	});