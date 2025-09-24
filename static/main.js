Webcam.attach('#camera');
  var image_taken;

  function take_photo() {
	  Webcam.snap( function(data_uri) {
		  document.getElementById("camera").innerHTML = '<img src="'+data_uri+'"/>';
      image_taken = data_uri;
      document.getElementById("capture-btn").style.display = "none";
      document.getElementById("ac").style.display = "inline";
	  } );
  }

  function s(){
    if(image_taken != null){
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/image", true);
      xhr.send(image_taken);
      loading();
    }
    else{alert("Take a photo first");}
  }