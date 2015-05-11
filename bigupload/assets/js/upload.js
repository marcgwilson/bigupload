var videoFile = null;
var CHUNK_SIZE = 1024 * 1024 * 5;
var cancel_button = document.getElementById('cancel_upload');
var upload_button = document.getElementById("start_upload");

cancel_button.onclick = cancelHandler;
upload_button.onclick = uploadHandler;

function cancelHandler() {
  videoFile = null;
  document.getElementById('list').innerHTML = '';
  $('#start_upload').addClass("disabled");
  $('#cancel_upload').addClass("disabled");
}

function uploadFile(token, index) {
  var start = index * CHUNK_SIZE;
  var stop = Math.min((index + 1) * CHUNK_SIZE, videoFile.size + 1);
  var blob = videoFile.slice(start, stop);
  var formData = new FormData();
  formData.append('chunk', blob, videoFile.name);
  formData.append('token', token);

  $.ajax({
      url: "/api/upload/",
      data: formData,
      async: true,
      cache: false,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(evt) {
        console.log("index: " + index);
        console.log("math.ceil: " + Math.ceil(videoFile.size / CHUNK_SIZE));
        if(videoFile != null && index < Math.ceil(videoFile.size / CHUNK_SIZE)) {
          console.log("upload again!");
          uploadFile(token, index + 1);
        } else {
          cancelHandler();
        }
        console.log("SUCCESS POSTING CHUNK");
      },
      error: function(evt) {
          console.log("ERROR");
      },
      progress: function(evt) {
          console.log("PROGRESS");
      }
  });
}

function getToken() {
  $.ajax({
      url: "/api/upload/token.json",
      async: true,
      cache: false,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(evt) {
          console.log("SUCCESS: " + evt.token);
          uploadFile(evt.token, 0);
      },
      error: function(evt) {
          console.log("ERROR");
      },
      progress: function(evt) {
          console.log("PROGRESS");
      }
  });
}

function uploadHandler() {
  getToken();
};

function handleFileSelect(evt) {
  evt.stopPropagation();
  evt.preventDefault();

  var files = evt.dataTransfer.files; // FileList object.

  // files is a FileList of File objects. List some properties.
  var output = [];
  for (var i = 0, f; f = files[i]; i++) {
      var general_type = f.type.split('/')[0];
      // console.log(general_type);
      var s = 'glyphicon glyphicon-leaf';
      if(general_type == 'video') {
          s = 'glyphicon glyphicon-film';
      }

      if((general_type == 'video' && videoFile == null)) {
          output.push('<li><span class="', s,'"></span> <strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                f.size, ' bytes, last modified: ',
                f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                '</li>');
      }

      if(general_type == 'video') {
          videoFile = f;
      }
  }

  if(videoFile != null) {
      $('#start_upload').removeClass("disabled");
      $('#cancel_upload').removeClass("disabled");
  }

  $('#list').append(output.join(''));
}

function handleDragOver(evt) {
  evt.stopPropagation();
  evt.preventDefault();
  evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

// Setup the dnd listeners.
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);
