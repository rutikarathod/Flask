
function check() {
  var pass = document.getElementById("password").value;
  
  //check empty password field
  if (pass == "") {
      document.getElementById("message").innerHTML = "Fill the password Field please!";
      return false;
  }

  //minimum password length validation
  if (pass.length < 7) {
      document.getElementById("message").innerHTML = "Password length must be 7 characters";
      return false;
  }

  //maximum length of password validation
  if (pass.length > 10) {
      document.getElementById("message").innerHTML = "Password length must be 7 characters";
      return false;
  }

 
  {
      document.getElementById("message").innerHTML=""
      return true;
  }
}


function chkfirst()
{
    var first_name = document.getElementById("chkfirstnm").value;
    if(first_name == "")
    {
        document.getElementById("chfirstnm").innerHTML = "Fill the first name please!";
        return false;
    }
    else
    {
        document.getElementById("chfirstnm").innerHTML = "";
        return true;
    }

}



function lastname()
{

    var last_name = document.getElementById("lastnm").value;
    if(last_name == "")
    {
        document.getElementById("lasnm").innerHTML = "Fill the last name please!";
        return false;
    }
    else
    {
        document.getElementById("lasnm").innerHTML = "";
        return true;
    }


}
function mobile() {
    var mob = document.getElementById("mobileno").value;

    // check empty mobilenumber field
    if (mob == "") {
        document.getElementById("mno").innerHTML = "Fill the Mobile Number Field";
        return false;
    } //minimum mobile number length validation
    if (mob.length < 10) {
        document.getElementById("mno").innerHTML = "Mobile Number length must be 10 characters";
        return false;
    }

    //maximum length of mobile number validation
    if (mob.length > 10) {
        document.getElementById("mno").innerHTML = "mobile Number length must be 10 characters";
        return false;
    } 
    else {
        document.getElementById("mno").innerHTML = "";
        return true;
    }
}

function chkadd(){
    var address = document.getElementById("add").value;

    if(address == "")
    {
        document.getElementById("addrs").innerHTML = "please Fill the address Field !";
        return false;
    }
    else{
        document.getElementById("addrs").innerHTML = "";
        return true;
    }
}

function chkcity(){
    var city = document.getElementById("cityy").value;

    if(city == "")
    {
        document.getElementById("cityr").innerHTML = " Please Fill the city Field  !"
        return false;
    }
    else{
        document.getElementById("cityr").innerHTML = "";
        return true;
    }
}

function chkzip() {
    var zipcode = document.getElementById("zip").value;

    if(zipcode == ""){
        document.getElementById("zipc").innerHTML = "Please Fill The Zipcode  !"
        return false;

    }
    if (zipcode.length < 6) {
        document.getElementById("zipc").innerHTML = "zipcode Number length must be 6 characters";
        return false;
    }
    if (zipcode.length > 6) {
        document.getElementById("zipc").innerHTML = "zipcode Number length must be 6 characters";
        return false;
    } 
    else {
        document.getElementById("zipc").innerHTML = "";
        return true;
    }

}
function chkuname(){
    var username = document.getElementById("usernm").value;

    if(username == "")
    {
        document.getElementById("unm").innerHTML = "Please Fill the Username Field  !"
        return false
    }
    else{
        document.getElementById("unm").innerHTML=""
        return true;
    }
}

function chkemail(){
    var email= document.getElementById("email").value;
    if(email=="")
    {
        document.getElementById("usrem").innerHTML="Please Fill The Email Field  !"
        return false;
    }
    else{
        document.getElementById("usrem").innerHTML=""
        return true;
    }
    
}

function chkstate(){
    var state = document.getElementById("stat").value;

    if(state == "")
    {
        document.getElementById("statc").innerHTML = "Please Fill the State Field  !"
        return false;
    }
    
    else{
        document.getElementById("statc").innerHTML = "";
        return true;
    }
}



function age() {
    var date = document.getElementById("dateob").value;
    var dob = new Date(date);
    if(date==null || date=='') {
      document.getElementById("dateof").innerHTML = "please Choose a date !";  
      return false; 
    }
    
    else
    { 
        var month_diff = Date.now() - dob.getTime();
        var age_dt = new Date(month_diff); 
        var year = age_dt.getUTCFullYear();
        var age = Math.abs(year - 1970);
        
        if(age < 18)
        {
            document.getElementById("dateof").innerHTML = "Eligibility 18 years ONLY ";  
            return false; 
        }
        if(age > 50){
            document.getElementById("dateof").innerHTML = "your age must be between 50";  
            return false; 
        }
        else{
        document.getElementById("dateof").innerHTML = "";
        return true;
        }
    }
}

function imgup(){
    var proimg = document.getElementById("profile").value;
    var filePath = proimg.value;
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    if(proimg == "")
    {
        document.getElementById("imagepro").innerHTML = "No Choosen file !"
        return false;
    }
    if (!allowedExtensions.exec(filePath))
    {
        document.getElementById("imagepro").innerHTML = "**Invalid format";
        fileInput.value = '';
        return false;
    }
    if (proimg.files[0].size > 1048576)
    {
         document.getElementById("imagepro").innerHTML = "**Images size should be less than 1 MB";
    }

    else{
        document.getElementById("imagepro").innerHTML = "";
        return true;
    }
}

var male = document.getElementById("ma");
var female = document.getElementById("fa");
var checked = document.getElementById("sel").innerHTML;
if(checked == "male")
{
    male.click()
}
else if(checked == "female")
{
    female.click()
}
else
{}


function fileupload1() {
    var upload = document.getElementById("fileupload").value;
    // check empty fileupload field
    if (upload == "") {
        document.getElementById("files").innerHTML = "Required to attach file of birth cirtificate";
        return false;
    }
    if (!/\.pdf$/i.test(upload)) {
        document.getElementById("files").innerHTML = "Attach only pdf format file";
        return false;
    }
    else 
    {
        document.getElementById("files").innerHTML = "";
        return true;
    }
}



  

  $(document).ready(function () {
    $('#example').DataTable();
});

