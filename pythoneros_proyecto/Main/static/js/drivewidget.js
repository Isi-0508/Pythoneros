/*function doGet(){
  var html = HtmlService.createTemplateFromFile('ventdrive');
  var output = html.evaluate();
  return output;
}

function uploadfiles(obj){
  var file = Utilities.newBlob(obj.bytes, obj.mimeType, obj.filename);
  var folder = DriveApp.getFolderById('1YzuiJTGv6eDysHIK6wgJOQet-mdEwxZE');
  var createFile = folder.createFile(file);
  return createFile.getId();
}
*/

function FileUpload(img, file){
    var reader = new FileReader();
    reader.onload = function(event) {

        const formData = new FormData();
        formData.append("file", file);

        fetch("/upload-drive/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": csrftoken }
        })
        .then(r => r.json())
        .then(data => console.log("ID en Drive:", data.file_id))
        .catch(err => console.error(err));
    };

    reader.readAsArrayBuffer(file);
}
