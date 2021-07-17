window.onload = function() {
    document.getElementById("message").focus();
    
  };

  function check(){
    var msg=document.getElementById("message").value;
    if( msg=="" || msg[0]==" "){
      return false;
    }
  }