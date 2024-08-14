function trim(value){
  return value.replace(/^\s*|\s*$/g, '');
}

//Define a function to get the written cookie value
function getCookie(name){
  var data = document.cookie.split(';');
  for (var i=0; i<data.length; i++){
    var keyValue = data[i].split('=');
    if (trim(keyValue[0]) == name){
      return decodeURIComponent(trim(keyValue[1]))
    }
  }
  return null; // Null if there is no cookie with that name
}
