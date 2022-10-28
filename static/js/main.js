



			
function SendMotorSignal (comm){

	var fd = new FormData();
	fd.append('mc', comm);

    axios({
    method: "post",
    url: "/motor_command",
    data:fd,
    headers: { "Content-Type": "multipart/form-data" },
    })
  .then(function (response) {
    //handle success
  })
  .catch(function (response) {
    //handle error
  });	
}

document.addEventListener('keydown', (event) => {
  var name = event.key;
  var code = event.code;
  // Alert the key name and key code on keydown
  
  if (name === "ArrowRight"){
    SendMotorSignal('R')
  }else if (name === "ArrowDown"){
    SendMotorSignal('NAZ')
  }else if (name === "ArrowLeft"){
    SendMotorSignal('L')
  }else if (name === "ArrowUp"){
    SendMotorSignal('V')
  }
  
  // console.log(name )

}, false);





