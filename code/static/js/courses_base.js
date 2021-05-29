$('.upload-file').on('hidden.bs.modal', function (event) {
    $("body").addClass("modal-open");
})
//mouse hold message show: title
$(function () {
    $('.CILOs-description').tooltip();
});

function descrption_update(obj) {
    var e = obj;
    $(e).attr("title", document.getElementById($(e).attr('id')).value)
}

function edit_get_line_nums() {
    var num = $("#edit-CILOs-table .Edit-CILOs-tbale-tr").length;
    var text1 =
        '<div class="input-group mb-3">\
        <div class="input-group-prepend">\
            <div class="input-group-text"><input type="checkbox" class="Related_CILOs_CheckBox" aria-label="Checkbox for following text input" value="'
    var text2 = '" onchange="edit_set_new_course_Related_CILOs_value(this)" >\
            </div>\
        </div><input type="text" class="form-control related-CILOs-dropbox-value" placeholder="" aria-label="Text input with checkbox" value="'
    var text3 = '" disabled></div>'
    $(".edit-Related-CILOs-dropmenu").children().remove();
    for (var i = 1; i <= num; i++) {
        $(".edit-Related-CILOs-dropmenu").append(text1 + i + text2 + i + text3)
    }
}

$(document).ready(function () {
    $("#Assessment-methods-add").click(function () {
        var append_text =
            '<tr class="Edit-assessment-methods-tbale-tr" style="text-align: center"; >\
                            <td><input type="text" class="form-control edit-Assessment-name" placeholder="please input name" value="" aria-label=""\
                                    aria-describedby="basic-addon1" style="text-align: center;"></td>\
                            <td>\
                                <div class="input-group Related-CILOs-input"><input type="text" class="form-control Related-CILOs-input-area"\
                                        placeholder="please choose CILOs" value="" aria-label="" aria-describedby="basic-addon2"\
                                        style="text-align: center;" disabled>\
                                    <div class="input-group-append">\
                                        <div class="dropdown" style="display: inline; ">\
                                            <button class="btn btn-outline-secondary dropdown-toggle" data-toggle="dropdown"\
                                                aria-expanded="false" style="float:right"></button>\
                                            <div class="dropdown-menu edit-Related-CILOs-dropmenu" aria-labelledby="dropdownMenuLink"></div>\
                                        </div>\
                                    </div>\
                                </div>\
                            </td>\
                            <td><input type="text" class="form-control percentage-input" placeholder="please input percentage" value="" aria-label=""\
                                    aria-describedby="basic-addon1" style="text-align: center;"></td>\
                            <td><button type="button" class="btn btn-light" onclick="minus(this)"><i class="fa fa-minus"></i></button></td>\
                        </tr>';
        $("#edit-Assessment-methods-table").append(append_text);
        edit_get_line_nums();
    });
});
function minus(obj) {
    var e = obj;
    $(e).parent().parent().remove();
}

var edit_related_CILOs_text = ""
function edit_set_new_course_Related_CILOs_value(obj) {
    var e = obj
    edit_related_CILOs_text = ""
    //$(e).parents(".Related-CILOs-dropmenu").css({"color":"red","border":"2px solid red"})
    //text += $("#Assessment-methods-table").find(".Related_CILOs_CheckBox",":checked").length
    $(e).parents(".edit-Related-CILOs-dropmenu").find(":checked").each(function () {
        //edit_related_CILOs_text += $(this).parents(".input-group").find(".related-CILOs-dropbox-value").css({"color":"red","border":"2px solid red"})
        if (edit_related_CILOs_text === "") {
            edit_related_CILOs_text += + $(this).val()
        } else {
            edit_related_CILOs_text += "," + $(this).val()
        }
    })
    $(e).parents(".Related-CILOs-input").find(".Related-CILOs-input-area").attr("value", edit_related_CILOs_text)

}
var edit_cilo_index = 0;
var Related_cilos
function edit_read(obj) {
    edit_cilo_index = 0;
    var e = $(obj).parents(".Action-column")
    $("#edit-Course-name").attr("value", e.siblings(".Course-name").attr("value"))
    $("#edit-Course-name").text(e.siblings(".Course-name").text())
    $("#edit-Course-code").text(e.siblings(".Course-code").text())
    $("#edit-CILOs-table").find(".Edit-CILOs-tbale-tr").remove()
    $("#edit-CILOs-table").append(e.find(".course-hide-CILOs-table").html())
    $("#edit-CILOs-table").attr("value", e.find(".course-hide-CILOs-table").attr("id"))
    $("#edit-CILOs-table").find(".CILOs-description").each(function () {
        $(this).attr("id", "edit-cilo-index-" + edit_cilo_index)
        edit_cilo_index++
    })
    $("#edit-CILOs-table").find(".CILOs-description").each(function () {
        descrption_update($(this))
    })
    $("#edit-Assessment-methods-table").find(".Edit-assessment-methods-tbale-tr").remove()
    $("#edit-Assessment-methods-table").append(e.find(".course-hide-assessment-methods-table").html())
    $("#edit-Assessment-methods-table").attr("value", e.find(".course-hide-assessment-methods-table").attr("id"))
    edit_get_line_nums()
    $("#edit-Assessment-methods-table").find(".Related-CILOs-input").each(function () {
        Related_cilos = $(this).find(".Related-cilo-dropdown-button").val().split(",")
        $(this).find(".Related_CILOs_CheckBox").each(function () {
            for (var i = 0; i < Related_cilos.length; i++) {
                if ($(this).val() == Related_cilos[i]) {
                    $(this).attr("checked", "checked")
                    break;
                }
            }
        })
    })
}

var edit_json = {}
var json_temp = {}
var edit_cilos_json;
var edit_assessment_json;
var edit_assessment_counter;
var edit_assessment_related;
function edit_course() {
    edit_json = {}
    edit_cilos_json = new Array()
    edit_json.course_id = $("#edit-Course-name").attr("value")
    edit_json.effective_since = $("#effective-course-year").val()
    $("#edit-CILOs-table").find(".Edit-CILOs-tbale-tr").each(function () {
        json_temp = {}
        json_temp.cilo_index = $(this).find(".CILO-order").attr("value")
        json_temp.cilo_description = $(this).find(".CILOs-description").val()
        edit_cilos_json.push(json_temp)
    })
    edit_json.cilos = edit_cilos_json

    edit_assessment_json = new Array()
    edit_assessment_counter = 1;
    $("#edit-Assessment-methods-table").find(".Edit-assessment-methods-tbale-tr").each(function () {
        json_temp = {}
        json_temp.method_index = edit_assessment_counter;
        edit_assessment_counter++;
        json_temp.method_name = $(this).find(".edit-Assessment-name").val()
        edit_assessment_related = new Array();
        $(this).find(".Related_CILOs_CheckBox").each(function () {
            if ($(this).prop("checked") == true) {
                edit_assessment_related.push($(this).val())
            }
        })
        json_temp.cilos_addressed = edit_assessment_related
        json_temp.weight = $(this).find(".percentage-input").val()
        edit_assessment_json.push(json_temp)
    })
    edit_json.assessment_methods = edit_assessment_json
    $.ajax({
        type: "PATCH",
        url: "/api/v1/courses",
        async: false,
        data: JSON.stringify(edit_json),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            console.log(data)
            $('#messageModal').find(".modal-title").text("success")
            $('#messageModal').find(".modal-body").html('<p>' + 'Course modified successfully.' + '</p>')
            $('#messageModal').modal('show')
            //window.location.reload()
            $("#dialog-comfirm-button").on("click", function () {
                window.location.reload()
            })
        },
        error: function (jqXHR) {
            //alert("error："+ jqXHR.status);
            //alert(jqXHR.responseJSON.error)
            $('#messageModal').find(".modal-title").text("error")
            $('#messageModal').find(".modal-body").html('<p>' + jqXHR.responseJSON.error + '</p>')
            $('#messageModal').modal('show')
        }
    })

    console.log(edit_json)
}


function set_import_type(type) {
    $("#import-file-type").attr("value", type)
}

$(".custom-file-input").on("change", function () {
    var file_name = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(file_name);
});

function upload() {
    var file = $('#customFile').val()
    if (file == '') {
        $('#messageModal').find(".modal-title").text("error")
        $('#messageModal').find(".modal-body").html('<p>' + "Please choose a file." + '</p>')
        $('#messageModal').modal('show')
        return false
    }
    var fileName = file.substring(file.lastIndexOf(".") + 1).toLowerCase();
    if (fileName != "xls" && fileName != "xlsx") {
        $('#messageModal').find(".modal-title").text("error")
        $('#messageModal').find(".modal-body").html('<p>' + "Please choose .xls or .xlsx file." + '</p>')
        $('#messageModal').modal('show')
        return false
    }
    if ($('#customFile')[0].files[0].size > 524288) {
        $('#messageModal').find(".modal-title").text("error")
        $('#messageModal').find(".modal-body").html('<p>' + "File size must be smaller than 512KB." + '</p>')
        $('#messageModal').modal('show')
        return false
    }

    var formData = new FormData();
    formData.append("file", $('#customFile')[0].files[0])
    $.ajax({
        type: "POST",
        url: "/api/v1/excel_parser",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data)
            if (typeof (data.content) == "undefined") {
                $('#messageModal').find(".modal-title").text("error")
                $('#messageModal').find(".modal-body").html('<p>' + "Please check the file." + '</p>')
                $('#messageModal').modal('show')
                return false
            }
            switch ($("#import-file-type").attr("value")) {
                case '1':
                    for (let i = 0; i < data.content.length >= $("#edit-CILOs-table .Edit-CILOs-tbale-tr").length ? $("#edit-CILOs-table .Edit-CILOs-tbale-tr").length : data.content.length; i++) {
                        //const element = data.content[i].description;
                        if (typeof (data.content[i].description) == "undefined") {
                            $("#upload-file-modal").modal('hide')
                            return false
                        }
                        $("#edit-cilo-index-" + i).val(data.content[i].description)
                    }
                    break;
                case '2':
                    //var line_num_temp = $("#edit-Assessment-methods-table .Edit-assessment-methods-tbale-tr").length
                    for (let i = 0; i < data.content.length; i++) {
                        //const element = data.content[i].description;
                        if (typeof (data.content[i].name) == "undefined" || typeof (data.content[i].percentage) == "undefined") {
                            $("#upload-file-modal").modal('hide')
                            return false
                        }
                        $("#Assessment-methods-add").trigger('click');
                        $("#edit-Assessment-methods-table .Edit-assessment-methods-tbale-tr").eq(i).find(".edit-Assessment-name").val(data.content[i].name)
                        $("#edit-Assessment-methods-table .Edit-assessment-methods-tbale-tr").eq(i).find(".percentage-input").val(data.content[i].percentage)
                    }
                    break;
                case '3':
                    for (let i = 0; i < data.content.length; i++) {
                        //const element = data.content[i].description;
                        if (typeof (data.content[i].description) == "undefined") {
                            $("#upload-file-modal").modal('hide')
                            return false
                        }
                        $("#CILOs-add").trigger('click');
                        $("#CILOs-table .new-CILOs-tbale-tr-value:last").find(".CILOs-description").val(data.content[i].description)
                    }
                    break;
                case '4':
                    for (let i = 0; i < data.content.length; i++) {
                        //const element = data.content[i].description;
                        if (typeof (data.content[i].name) == "undefined" || typeof (data.content[i].percentage) == "undefined") {
                            $("#upload-file-modal").modal('hide')
                            return false
                        }
                        $("#new-Assessment-methods-add").trigger('click');
                        $("#Assessment-methods-table .new-Assessment-methods-tr:last").find(".new-Assessment-name").val(data.content[i].name)
                        $("#Assessment-methods-table .new-Assessment-methods-tr:last").find(".new-Assessment-percentage").val(data.content[i].percentage)
                    }
                    break;
                default:
                    console.log("import failed")
                    break;
            }
            $("#upload-file-modal").modal('hide')
        },
        error: function (jqXHR) {
            //alert("error："+ jqXHR.status);
            //alert(jqXHR.responseJSON.error)
            $('#messageModal').find(".modal-title").text("error")
            $('#messageModal').find(".modal-body").html('<p>' + jqXHR.responseJSON.error + '</p>')
            $('#messageModal').modal('show')
        }
    })
}
