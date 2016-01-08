

var bio = { "name" : "John Doe" , "role" : "Web Developer", "contacts" : {"email" : "johndoe@email.com", "github" : "gittyup", "twitter" : "@javajohn",  
		"mobile" : "555-555-5555", "location" : "New York City, NY"}, "pictureURL" : "images/fry.jpg", "welcome" : "Hello world!", 
		"skills" : ["Awesome", "funny", "Smart", "programming"], "display" : function() {
	if (bio.skills.length > 0){
		$("#header").append(HTMLskillsStart);
		for (skill in bio.skills) {

			var formattedSkills = HTMLskills.replace("%data%", bio.skills[skill]);
			$("#skills").append(formattedSkills);
		
		}
	}
}};
var formattedName = HTMLheaderName.replace("%data%", bio.name);
var formattedRole = HTMLheaderRole.replace("%data%", bio.role);
var formattedEmail = HTMLemail.replace("%data%", bio.contacts.email);
var formattedMobile = HTMLmobile.replace("%data%", bio.contacts.mobile);
var formattedTwitter = HTMLtwitter.replace("%data%", bio.contacts.twitter);
var formattedGithub = HTMLgithub.replace("%data%", bio.contacts.github);
var formattedPicture = HTMLbioPic.replace("%data%", bio.pictureURL);
var formattedWelcome = HTMLwelcomeMsg.replace("%data%", bio.welcome);
var formattedLocation = HTMLlocation.replace("%data%", bio.contacts.location);

var education = {"schools" :[
{"name": "USC", "dates" : "1994-1996", "degree" : "BS", "location" : "Los Angeles", "majors": "CS"}, 
{"name": "City College", "dates" : "1992-1994", "degree" : "Associate of Science", "location" : "Austin, TX", "majors" : "CS"}],

"onlineCourses" : [ {"school": "Udacity", "date" : "2015", "title" : "Intro to Programming Nano-degree", "url" : "http://www.udacity.com"}],
"displayschools" :
function() {$("#education").append(HTMLschoolStart);
for (school in education.schools) {
	var formattedschoolname = HTMLschoolName.replace("%data%", education.schools[school].name);
	var formattedschoollocation = HTMLschoolLocation.replace("%data%", education.schools[school].location);
	var formattedschooldegree = HTMLschoolDegree.replace("%data%", education.schools[school].degree);
	var formattedschoolnamedegree = formattedschoolname + formattedschooldegree;
	var formattedschoolmajors = HTMLschoolMajor.replace("%data%", education.schools[school].majors);
	var formattedschooldates = HTMLschoolDates.replace("%data%", education.schools[school].dates);
	$(".education-entry:last").append(formattedschoolnamedegree, formattedschoollocation ,formattedschooldates, formattedschoolmajors);
}}, "displayonlineclasses" : function(){
$(".education-entry:last").append(HTMLonlineClasses);

for (onlinecourse in education.onlineCourses) {
	console.log(onlinecourse);
	var formattedonlinetitle = HTMLonlineTitle.replace("%data%", education.onlineCourses[onlinecourse].title);
	var formattedonlineschool = HTMLonlineSchool.replace("%data%", education.onlineCourses[onlinecourse].school);
	var formattedonlinedate = HTMLonlineDates.replace("%data%", education.onlineCourses[onlinecourse].date);
	var formattedtitleschool = formattedonlinetitle + formattedonlineschool;
	var formattedonlineurl = HTMLonlineURL.replace("%data%", education.onlineCourses[onlinecourse].url);
	var formattedonlineurl = formattedonlineurl.replace("#",education.onlineCourses[onlinecourse].url)
	$(".education-entry:last").append(formattedtitleschool, formattedonlinedate, formattedonlineurl);
}}
};




var work = { "jobs" : [{"position" : "Technical Support Manager", "employer" : "Big Phone Company", "years" : "2000 - current", 
			"location" : "St Louis, MO", "desc" : "Provide technical support for switch translaions."}, 
			{"position" : "Quality Control", "employer" : "Boeing", "years" : "1998-2000", 
			"location" : "Seattle, WA" , "desc" : "Tested electrical wiring harnesses for quality control."}], "display" : function(){
	$("#workExperience").append(HTMLworkStart);

	for (job in work.jobs) {

		
		var formattedWorkTitle = HTMLworkTitle.replace("%data%", work.jobs[job].position);
		var formattedWorkEmployer = HTMLworkEmployer.replace("%data%", work.jobs[job].employer);
		var formattedEmployerTitle = formattedWorkEmployer + formattedWorkTitle;
		var formattedWorkLocations = HTMLworkLocation.replace("%data%", work.jobs[job].location);
		var formattedDates = HTMLworkDates.replace("%data%", work.jobs[job].years);
		var formattedDescription = HTMLworkDescription.replace("%data%", work.jobs[job].desc);
		$(".work-entry:last").append(formattedEmployerTitle, formattedWorkLocations, formattedDates, formattedDescription);


	}
	
}
};



var projects = { "projects" : [{"title" : "Project 1", "dates" : "1999", "desc": "did a bunch of stuff", "image" : "images/197x148.gif"} , {
	"title" : "Project 2", "dates" : "2015", "desc": "even more stuff", "image" : "images/197x148.gif"
}], "display" : function(){

$("#projects").append(HTMLprojectStart);
for (project in projects.projects){

	var formattedProjectTitle = HTMLprojectTitle.replace("%data%", projects.projects[project].title);
	var formattedProjectDate = HTMLprojectDates.replace("%data%", projects.projects[project].dates);
	var formattedProjectDesc = HTMLprojectDescription.replace("%data%", projects.projects[project].desc);
	var formattedProjectImage = HTMLprojectImage.replace("%data%", projects.projects[project].image);
	$(".project-entry:last").append(formattedProjectTitle, formattedProjectDate, formattedProjectDesc, formattedProjectImage);


}}

}


$("#header").prepend(formattedRole);
$("#header").prepend(formattedName);


$("#header").append(formattedWelcome);
$("#header").append(formattedPicture);
var contactType = [ bio.contacts.email, bio.contacts.mobile, bio.contacts.github, bio.contacts.twitter, bio.contacts.location];
var contactinfo = [ formattedEmail, formattedMobile, formattedGithub, formattedTwitter, formattedLocation];
for (contact in contactType){
	if (typeof contactType[contact] != 'undefined') {
		$("#topContacts").append(contactinfo[contact]);
		$("#footerContacts").append(contactinfo[contact]);
	}
}


$("#main").append(internationalizeButton);

var inName = function(){
	var namearray = [];
	var name = bio.name;
	namearray=name.split(" ");
	var newname=namearray[0] + " " + namearray[1].toUpperCase();
	return newname;
}


eval(education.displayschools());
eval(education.displayonlineclasses());
eval(bio.display());

eval(work.display());
eval(projects.display());

$("#mapDiv").append(googleMap);
