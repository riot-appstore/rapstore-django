/*
 * Copyright (C) 2017-2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

var downloadIsRunning = false;

var isFirefox = typeof InstallTrigger !== 'undefined';
var isChrome = !!window.chrome && !!window.chrome.webstore;


// show pop up, before closing tab by running download
// https://stackoverflow.com/questions/6966319/javascript-confirm-dialog-box-before-close-browser-window
window.onbeforeunload = function (event) {

    if (downloadIsRunning) {

        var message = "Download is still running. Are you sure you want to leave?";
        if (typeof event == "undefined") {
            event = window.event;
        }
        if (event && downloadIsRunning) {
            event.returnValue = message;
        }
        return message;
    }
    else {
        // dont show a dialog when no download is running
        return null;
    }
};

// return true if everything went fine, false in case of failure
function doPrechecks() {

    // first check: is another download already running?
    if(downloadIsRunning) {
        showAlertDownloadProcessRunning();
        return false;
    }
    // second check: is the extension itself installed/ activated
    else if (!extensionAvailable) {
        showAlertNoExtension();
        return false;
    }
    // third check: check if the extension was able to connect to native messaging host
    else if (!nativeMessagingHostAvailable) {
        showAlertNoNativeMessagingHost();
        return false;
    }

    // all tests passed successfully
    return true;
}


function buildAndFlashCustom() {

    if (doPrechecks()) {
        buildAndFlashCustomPost();
    }
}


function buildAndFlashExample(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID) {

    if (doPrechecks()) {
        buildAndFlashExamplePost(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID);
    }
}


function buildAndDownloadExample() {
    // TODO: implement
}


function buildAndDownloadCustom() {
    // TODO: implement
}


function buildAndFlashCustomPost() {

    //https://stackoverflow.com/questions/8563240/how-to-get-all-checked-checkboxes
    var checkboxes = document.getElementsByName("module_checkbox");
    var checkboxesChecked = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            // add the IDs (retrieved from the database) to the array
            checkboxesChecked.push(checkboxes[i].value);
        }
    }

    var board = document.getElementById("board-selector").value;
    var main_file = document.getElementById("customTab_main_file_input").files[0];

    if (checkboxesChecked.length == 0) {

        alert("You need to select at least one module");
    }
    else if (main_file == null) {

        alert("You have to upload your main source file for your project!");
    }
    else {

        downloadIsRunning = true;
        setNavigationEnabled(false);

        var downloadButton = document.getElementById("customTab_buttonBuildFlash");
        var progressBar = document.getElementById("customTab_progressBar");

        downloadButton.disabled = true;
        progressBar.style.visibility = "visible";

        var formData = new FormData();
        for (var i = 0; i < checkboxesChecked.length; i++) {
            formData.append('selected_modules[]', checkboxesChecked[i]);
        }
        formData.append("board", board);
        formData.append("main_file_content", main_file, "main.c");

        // https://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously
        $.ajax({
            url: "/requests/request.py",
            type: "POST",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,

            error: function (xhr, ajaxOptions, thrownError) {

                downloadIsRunning = false;
                setNavigationEnabled(true);
                alert(thrownError);
            },
            success: function(response) {

                downloadIsRunning = false;
                setNavigationEnabled(true);

                var jsonResponse = null;
                try {
                    jsonResponse = JSON.parse(response);
                }
                catch(e) {
                    alert("Server sent broken JSON");
                    return;
                }

                var innerMessage = JSON.parse(jsonResponse.message);

                if(innerMessage != null && innerMessage.output_archive != null) {
                    downloadButton.className = "btn btn-success";
                    downloadButton.innerHTML = "Download"

                    if (isFirefox || isChrome) {
                        messageExtension("rapstore_install_image", jsonResponse);
                    }
                    else {
                        alert("Browser not supported yet, sry!");
                    }
                }
                else {
                    downloadButton.className = "btn btn-danger";
                    downloadButton.innerHTML = "Something went wrong"
                }

                //this.responseText has to be a json string
                document.getElementById("customTab_cmdOutput").innerHTML = jsonResponse.cmd_output;
            }
        });
    }
}


function buildAndFlashExamplePost(applicationID, progressDivID, progressBarID, panelID, buttonID, modalDialogID) {

    downloadIsRunning = true;
    setNavigationEnabled(false);

    var progressDiv = document.getElementById(progressDivID);
    var progressBar = document.getElementById(progressBarID);
    var panel = document.getElementById(panelID);
    var button = document.getElementById(buttonID);

    var modalDialog = document.getElementById(modalDialogID);
    var modalDialogBody = modalDialog.getElementsByClassName("modal-body")[0];
    var modalDialogFooter = modalDialog.getElementsByClassName("modal-footer")[0];

    progressDiv.style.visibility = "visible";
    progressBar.style.visibility = "visible";

    // reset
    panel.className = "panel panel-default";
    button.className = "btn btn-primary"

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {

        if (this.readyState == 4) {
            downloadIsRunning = false;
            setNavigationEnabled(true);
        }

        if (this.readyState == 4 && this.status == 200) {

            var jsonResponse = null;
            try {
                jsonResponse = JSON.parse(this.responseText);
            }
            catch(e) {
                alert("Server sent broken JSON");
                progressDiv.style.visibility = "hidden";
                progressBar.style.visibility = "hidden";
                return;
            }

            var innerMessage = JSON.parse(jsonResponse.message);

            if(innerMessage != null && innerMessage.output_archive != null) {
                panel.className = "panel panel-success";

                button.className = "btn btn-success";

                if (isFirefox || isChrome) {
                    messageExtension("rapstore_install_image", jsonResponse);
                }
                else {
                    alert("Browser not supported yet, sry!");
                }
            }
            else {
                panel.className = "panel panel-danger";

                button.className = "btn btn-danger";
                button.innerHTML = "Show error log";

                modalDialogBody.innerHTML = "<p>" + innerMessage.cmd_output + "</p>";
                modalDialogFooter.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal" onclick="sendMailToSupport(\'' + modalDialogID + '\')">Send log to support</button>' + modalDialogFooter.innerHTML;

                $('#' + modalDialogID + '').modal('show');
                button.onclick = function() {
                    $('#' + modalDialogID + '').modal('show');
                }
            }

            progressDiv.style.visibility = "hidden";
            progressBar.style.visibility = "hidden";
       }
    };

    xhttp.open("POST", "/requests/request_example.py", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    params = "";
    params += "application=" + applicationID;
    params += "&";
    params += "board=" + document.getElementById("board-selector").value;

    xhttp.send(params);
}




function disableAllFlashButtons(extensionAvailable, hostAvailable) {

    $('.build-and-flash-button').each(function() {

        $(this).removeClass('btn-primary');
        $(this).addClass('btn-default');

        if (!extensionAvailable) {
            $(this).attr("onclick", "showAlertNoExtension()");
        }
        else if (!hostAvailable) {
            $(this).attr("onclick", "showAlertNoNativeMessagingHost()");
        }
    });
}


function sendMailToSupport(modalDialogID) {

    var modalDialog = document.getElementById(modalDialogID);
    var modalDialogBody = modalDialog.getElementsByClassName("modal-body")[0];

    window.open("mailto:hendrik.ve@fu-berlin.de?subject=rapstore&body=" + encodeURIComponent(modalDialogBody.innerHTML) + "");
}


function setNavigationEnabled(enabled) {

    // https://stackoverflow.com/questions/20668880/bootstrap-tabs-pills-disabling-and-with-jquery
    if (enabled) {
        $(".nav li").removeClass('disabled');
        $(".nav li").find("a").attr("data-toggle","tab");
    }
    else {
        $(".nav li").addClass('disabled');
        $(".nav li").find("a").removeAttr("data-toggle");
    }
}


// https://codepen.io/CSWApps/pen/GKtvH
$(document).on('click', '.browse', function(){
    var file = $(this).parent().parent().parent().find('.file');
    file.trigger('click');
});
$(document).on('change', '.file', function(){
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});


(function(w, d){


  function LetterAvatar (name, size) {

    name  = name || '';
    size  = size || 60;

    var colours = [
        "#8d1821", "#6fbda5", "#a01b25", "#5bb499", "#bd202c",
        "#3fa788", "#c6414b", "#358d73", "#cd5760", "#2f7d66"
      ],

      nameSplit = String(name).toUpperCase().split(' '),
      initials, charIndex, colourIndex, canvas, context, dataURI;


    if (nameSplit.length == 1) {
      initials = nameSplit[0] ? nameSplit[0].charAt(0):'?';
    } else {
      initials = nameSplit[0].charAt(0) + nameSplit[1].charAt(0);
    }

    if (w.devicePixelRatio) {
      size = (size * w.devicePixelRatio);
    }

    charIndex     = (initials == '?' ? 72 : initials.charCodeAt(0)) - 64;
    colourIndex   = charIndex % colours.length;
    canvas        = d.createElement('canvas');
    canvas.width  = size;
    canvas.height = size;
    context       = canvas.getContext("2d");

    context.fillStyle = colours[colourIndex];
    context.fillRect (0, 0, canvas.width, canvas.height);
    context.font = Math.round(canvas.width/2)+"px Arial";
    context.textAlign = "center";
    context.fillStyle = "#FFF";
    context.fillText(initials, size / 2, size / 1.5);

    dataURI = canvas.toDataURL();
    canvas  = null;

    return dataURI;
  }

  LetterAvatar.transform = function() {

    Array.prototype.forEach.call(d.querySelectorAll('img[avatar]'), function(img, name) {
      name = img.getAttribute('avatar');
      img.src = LetterAvatar(name, img.getAttribute('width'));
      img.removeAttribute('avatar');
      img.setAttribute('alt', name);
    });
  };


  // AMD support
  if (typeof define === 'function' && define.amd) {

    define(function () { return LetterAvatar; });

    // CommonJS and Node.js module support.
  } else if (typeof exports !== 'undefined') {

    // Support Node.js specific `module.exports` (which can be a function)
    if (typeof module != 'undefined' && module.exports) {
      exports = module.exports = LetterAvatar;
    }

    // But always support CommonJS module 1.1.1 spec (`exports` cannot be a function)
    exports.LetterAvatar = LetterAvatar;

  } else {

    window.LetterAvatar = LetterAvatar;

    d.addEventListener('DOMContentLoaded', function(event) {
      LetterAvatar.transform();
    });
  }

})(window, document);
