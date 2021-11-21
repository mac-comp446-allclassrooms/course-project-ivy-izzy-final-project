function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .width(400)
                .attr('visibility', 'visible')
        };
        document.getElementById("blah").classList.remove('hidden')
        reader.readAsDataURL(input.files[0]);
    }
  }

  
function readURL2(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#file2')
                .attr('src', e.target.result)
                .width(400)
        };
        document.getElementById("file2").classList.remove('hidden')
        reader.readAsDataURL(input.files[0]);
    }
  }