function editNoteAction() {
    $('.open-EditNote').on({
        'click': function(event) {
            // Remove old modal, if any
            $("#editNote").remove();

            var pieceid = $(this).data('pieceid');

            $.ajax({
                type: "GET",
                url: "/note/" + pieceid,
                dataType: 'json',
                success: function (json) {
                    showModalAction(pieceid, json);
                },
                error: function() {
                    showModalAction(pieceid);
                }
            });

            return false;
        }
    });
}

function showModalAction(pieceid, json) {
    // Title string
    var titletext = ('Edit Note to Piece ' + pieceid);
    var notetext = '';

    // Get CURRENT text of note -- not necessarily what
    // it was when template was loaded
    if (json) {
        notetext = json.text;
    }

    // Outer div for modal.
    var modal = $("<div />", {
        "id": "editNote",
        "class": "modal fade",
        "tabindex": "-1",
        "role": "dialog",
        "aria-labelledby": "editNote",
        "aria-hidden": "true",
    }).appendTo("body");

    // First layer div
    var modal_dialog = $("<div />", {
        "class": "modal-dialog",
    }).appendTo(modal);

    // Second layer div
    var modal_content = $("<div />", {
        "class": "modal-content",
    }).appendTo(modal_dialog);

    // Modal header div
    var modal_header = $("<div />", {
        "class": "modal-header",
    }).appendTo(modal_content);

    // Modal header: button
    var modal_header_button = $("<button />", {
        "type": "button",
        "class": "close",
        "data-dismiss": "modal",
        "aria-hidden": "true",
        "text": "×",
    }).appendTo(modal_header);

    // Modal header: text
    var modal_header_text = $("<h3 />", {
        "class": "modal-title",
        "id": "editNoteLabel",
        "text": titletext,
    }).appendTo(modal_header);

    // Modal body div
    var modal_body = $("<div />", {
        "class": "modal-body",
    }).appendTo(modal_content);

    // Modal body: paragraph
    var modal_body_p = $("<p />", {
        "id": "modal-body-p",
    }).appendTo(modal_body);

    // Modal body: form's piece ID
    var modal_body_pieceid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "piece_id",
        "id": "piece-id",
        "value": pieceid,
    }).appendTo(modal_body_p);

    // Modal body: form's textarea
    var modal_body_textarea = $("<textarea />", {
        "form": "modal-form",
        "name": "text",
        "rows": "10",
        "id": "note-textarea",
        "style": "width:100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;",
        "text": notetext,
    }).appendTo(modal_body_p);

    // Modal footer div
    var modal_footer = $("<div />", {
        "class": "modal-footer",
    }).appendTo(modal_content);

    var modal_footer_close = $("<button />", {
        "type": "button",
        "class": "btn btn-default",
        "data-dismiss": "modal",
        "text": "Close",
    }).appendTo(modal_footer);

    var modal_footer_save = $("<button />", {
        "form": "modal-form",
        "type": "submit",
        "id": "modal-save",
        "class": "btn btn-primary",
        "data-dismiss": "modal",
        "text": "Save changes",
    }).appendTo(modal_footer);

    $("#editNote").modal({
        "backdrop": "static",
    });

    $( "#modal-save" ).on({
        'click': function(event) {
            $('#modal-form').submit();
            event.preventDefault();
        }
    });
}

function submitNoteAction() {
    $( "#modal-form" ).submit(function( event ){
        var form = $(this);
        var serialized_data = form.serialize();
        var pieceid = document.getElementById("piece-id").value;
        $.ajax({
            type: "POST",
            url: "/notes/",
            data: serialized_data,
        });

        // If it was an Add Note button, make it now an Edit Note button
        // by removing "primary" class and changing text
        var button = document.getElementById("button-" + pieceid);
        button.className = "btn btn-info open-EditNote";
        button.innerHTML = "Edit Note";
        button.title = "Edit Note to " + pieceid;


        event.preventDefault();
    });
}
