function doGet(){
  var html = HtmlService.createTemplateFromFile('ventdrive');
  var output = html.evaluate();
  return output;
}

function uploadfiles(obj){
  var file = Utilities.newBlob(obj.bytes, obj.mimeType, obj.filename);
  var folder = DriveApp.getFolderById('');
  var createFile = folder.createFile(file);
  return createFile.getId();
}