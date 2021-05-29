
//fix the problem of modal
	$('.define-box').on('hidden.bs.modal', function (event) {
		$("body").addClass("modal-open");
	})


	//CILOs add function
	$(document).ready(function () {
		$("#CILOs-add").click(function () {
			var index = $("#CILOs-table .new-CILOs-tbale-tr").length;
			var CILOsAdditon = //style="display:none"
				'<tr class="new-CILOs-tbale-tr new-CILOs-tbale-tr-value" style="text-align: center;">\
				<td class="CILO-order" value="'+ index + '">CILO-' + index + '</td>\
				<td><input type="text" class="form-control CILOs-description" id="CILOs-description-' + index + '" title=""\
						oninput="descrption_update($(this))" placeholder="please input {{ get_str("DESCRIPTION") }}" value=""\
						aria-label="" aria-describedby="basic-addon1" data-toggle="tooltip" style="text-align: center;"></td>\
				<td><button type="button" class="btn btn-info" id="CILOs-define" data-toggle="modal" data-target=".define-box" onclick="read_CILOs(this)"> {{get_str("DEFINE") }}</button>\
					<table class="CILOs-hide-table" id="CILOs-hide-table-'+ index + '" style="display:none">\
						<tr style="text-align: center;">\
								<th style="display: none;">\
									CILOs unique ID\
								</th>\
								<th>\
									<label>{{ get_str("COURSE") }}</label>\
								</th>\
								<th>\
									<label>{{ get_str("CILO") }}</label>\
								</th>\
								<th style="width: 30px;">\
									<label>{{ get_str("ACTION") }}</label>\
								</th>\
							</tr>\
						</table>\
				</td>\
				<td><button type="button" class="btn btn-light CILOs-minus" onclick="CILOs_remove(this)"><i class="fa fa-minus"></i></button></td>\
			</tr>';
			$("#CILOs-table").append(CILOsAdditon);
			get_line_nums();
		});
	});

	//cilos define read function
	function read_CILOs(obj) {
		var e = obj
		var id_text = $(e).parent().find(".CILOs-hide-table").attr("id");
		var table_concent = $(e).parent().find(".CILOs-hide-table").html();
		$(".define-box-added-table").children().remove();
		$(".define-box-added-table").attr("value", id_text);
		$(".define-box-added-table").append(table_concent);
		//console.log($(".define-box-added-table").attr("value"))
	}

	function write_CILOs() {
		var id = "#" + $(".define-box-added-table").attr("value");
		var update_content = $(".define-box-added-table").html();
		$(id).children().remove();
		$(id).append(update_content);
		update_Pre_requisites();
	}

	var same_CILO_flag = false;
	function CILOs_define_page_add(obj) {
		var e = obj;
		var e2 = $(e).parents(".CLIOs-define-tr")
		same_CILO_flag = false;
		$(".define-box-added-table").find(".CILO-ID-td").each(function () {
			if ($(this).text() === $(e2).find(".CILO-ID-td").text()) {
				alert("This CILO is already added!");
				$(e2).remove();
				same_CILO_flag = true;
			}
		})
		if (same_CILO_flag) { return }
		var minus = '<button type="button" class="btn btn-light" onclick="CILOs_define_page_minus(this)">\
										<i class="fa fa-minus"></i>\
									</button>'
		$(e).parents(".CILOs-button-td").html(minus);
		var content = $(e2).html()
		var content_text = '<tr class="CLIOs-define-tr" style="text-align: center;">' + content + '</tr>'
		$(".define-box-added-table").append(content_text);
		$(e2).remove();
	}

	function CILOs_define_page_minus(obj) {
		var e = obj;
		var e2 = $(e).parents(".CLIOs-define-tr")
		var plus = '<button type="button" class="btn btn-light" onclick="CILOs_define_page_add(this)">\
										<i class="fa fa-plus"></i>\
									</button>'
		$(e).parents(".CILOs-button-td").html(plus);
		var content = $(e2).html()
		var content_text = '<tr class="CLIOs-define-tr" style="text-align: center;">' + content + '</tr>'
		$(".define-box-result-table").append(content_text);
		$(e2).remove();
	}

	var Pre_requisites_list
	function update_Pre_requisites() {
		Pre_requisites_list = new Array();
		$("#CILOs-table").find(".course-name-td").each(function () {

			Pre_requisites_list.push($(this).text())
		})
		var temp_array = new Array();
		for (var i = 0; i < Pre_requisites_list.length; i++) {
			var flag = true;
			for (var j = 0; j < temp_array.length; j++) {
				if (temp_array[j] === Pre_requisites_list[i]) {
					flag = false;
					break;
				}
			}
			if (flag) {
				temp_array.push(Pre_requisites_list[i]);
			}
		}
		$("#Pre-requisites-table").find(".Pre-requisites-tr").remove();
		for (var i = 0; i < temp_array.length; i++) {
			$("#Pre-requisites-table").append('<tr class="Pre-requisites-tr" style="text-align: center;"><td>' + temp_array[i] + "</tr></td>")
		}
	}

	function term_select(obj) {
		var e = obj;
		$("#new-course-term").attr("value", $(e).text());
	}

	function edit_term_select(obj) {
		var e = obj;
		$("#edit-effective-course-term").attr("value", $(e).text());
	}

	function program_select(obj) {
		var e = obj;
		var text = $(e).text();
		$("#new-course-program").attr("value", text);
		$("#new-course-program").attr("aria-label", $(e).attr("value"));
	}
	function course_type_select(obj) {
		var e = obj;
		var text = $(e).text();
		$("#new-course-type").attr("value", text);
		$("#new-course-type").attr("aria-label", $(e).attr("value"));
	}


	function get_line_nums() {
		var num = $("#CILOs-table .new-CILOs-tbale-tr").length;
		var text1 =
			'<div class="input-group mb-3">\
			<div class="input-group-prepend">\
				<div class="input-group-text"><input type="checkbox" class="Related_CILOs_CheckBox" aria-label="Checkbox for following text input" value="'
		var text2 = '" onchange="set_new_course_Related_CILOs_value(this)" >\
				</div>\
			</div><input type="text" class="form-control related-CILOs-dropbox-value" placeholder="" aria-label="Text input with checkbox" value="'
		var text3 = '" disabled></div>'
		$(".Related-CILOs-dropmenu").children().remove();
		for (var i = 1; i < num; i++) {
			$(".Related-CILOs-dropmenu").append(text1 + i + text2 + i + text3)
		}
	}



	function CILOs_remove(obj) {
		minus(obj);
		update_CILOs_table();
		get_line_nums();
		$(".Related-CILOs-input-area").val("")
	}
	function set_search_type(obj) {
		$("#search-type-switch").attr("value", $(obj).attr("value"))
		$("#search-type-switch").text($(obj).text())
	}
	//add Assessment methods function
	$(document).ready(function () {
		$("#new-Assessment-methods-add").click(function () {
			var append_text =
				'<tr style="text-align: center"; class="new-Assessment-methods-tr">\
			<td><input type="text" class="form-control new-Assessment-name" placeholder="please input name" value="" aria-label=""\
					aria-describedby="basic-addon1" style="text-align: center;"></td>\
			<td>\
				<div class="input-group Related-CILOs-input"><input type="text" class="form-control Related-CILOs-input-area" placeholder="please choose CILOs" value=""\
						aria-label="" aria-describedby="basic-addon2" style="text-align: center;" disabled>\
					<div class="input-group-append">\
						<div class="dropdown" style="display: inline; ">\
							<button class="btn btn-outline-secondary dropdown-toggle" data-toggle="dropdown"\
								aria-expanded="false" style="float:right"></button>\
							<div class="dropdown-menu Related-CILOs-dropmenu" aria-labelledby="dropdownMenuLink"></div>\
						</div>\
					</div>\
				</div>\
			</td>\
			<td><input type="text" class="form-control new-Assessment-percentage" placeholder="please input percentage" value="" aria-label=""\
					aria-describedby="basic-addon1" style="text-align: center;"></td>\
			<td><button type="button" class="btn btn-light" onclick="minus(this)"><i class="fa fa-minus"></i></button></td>\
			</tr>';
			$("#Assessment-methods-table").append(append_text);
			get_line_nums();
		});
	});






	function update_CILOs_table() {
		let CILOsIndex = 1
		$("#CILOs-table").find("td.CILO-order").html(function () {
			var text = "CILO-" + CILOsIndex
			$(this).attr("value", CILOsIndex)
			CILOsIndex++
			return text
		})
		CILOsIndex = 1
		$("#CILOs-table").find("input.CILOs-description").attr("id", () => {
			var text = "CILOs-description-" + CILOsIndex
			CILOsIndex++
			return text
		})
	}

	//function(){ return $(this).parents(".input-group").find(".related-CILOs-dropbox-value").attr("value")}
	var related_CILOs_text = ""
	function set_new_course_Related_CILOs_value(obj) {
		var e = obj
		related_CILOs_text = ""
		//$(e).parents(".Related-CILOs-dropmenu").css({"color":"red","border":"2px solid red"})
		//text += $("#Assessment-methods-table").find(".Related_CILOs_CheckBox",":checked").length
		$(e).parents(".Related-CILOs-dropmenu").find(":checked").each(function () {
			//related_CILOs_text += $(this).parents(".input-group").find(".related-CILOs-dropbox-value").css({"color":"red","border":"2px solid red"})
			if (related_CILOs_text === "") {
				related_CILOs_text += + $(this).val()
			} else {
				related_CILOs_text += "," + $(this).val()
			}
		})
		$(e).parents(".Related-CILOs-input").find(".Related-CILOs-input-area").attr("value", related_CILOs_text)
	}




	//this function useless
	function edit_write() {

	}

	var add_json = {}
	var json_temp = {}
	var add_cilos_json;
	var add_assessment_json;
	var add_assessment_counter;
	var add_depending_cilos
	var add_assessment_related;

	function add_course() {
		//front 6 input
		add_json = {}
		json_temp = {}
		add_cilos_json = new Array();
		add_json.course_name = $("#new-course-title").val()
		add_json.course_code = $("#new-course-code").val()
		add_json.course_type_id = $("#new-course-type").attr("aria-label")
		add_json.program_id = $("#new-course-program").attr("aria-label")
		add_json.effective_since = $("#new-course-year").val()
		//CILOs table
		$("#CILOs-table").find(".new-CILOs-tbale-tr-value").each(function () {
			add_depending_cilos = new Array();
			json_temp = {}
			json_temp.cilo_index = $(this).find(".CILO-order").attr("value")
			json_temp.cilo_description = $(this).find(".CILOs-description").val()
			$(this).find(".CILO-ID-td").each(function () {
				add_depending_cilos.push($(this).text())
			})
			json_temp.cilo_description = add_depending_cilos
			add_cilos_json.push(json_temp)
		})
		add_json.cilos = add_cilos_json
		//Assessment table
		add_assessment_json = new Array();
		add_assessment_counter = 1;
		$("#Assessment-methods-table").find(".new-Assessment-methods-tr").each(function () {
			json_temp = {}
			json_temp.method_index = add_assessment_counter;
			add_assessment_counter++;
			json_temp.method_name = $(this).find(".new-Assessment-name").val();
			add_assessment_related = new Array();
			$(this).find(".Related_CILOs_CheckBox").each(function () {
				if ($(this).prop("checked") == true) {
					add_assessment_related.push($(this).val())
				}
			})
			json_temp.cilos_addressed = add_assessment_related
			json_temp.weight = $(this).find(".new-Assessment-percentage").val()
			add_assessment_json.push(json_temp)
		})
		add_json.assessment_methods = add_assessment_json
		$.ajax({
			type: "POST",
			url: "/api/v1/courses",
			async: false,
			data: JSON.stringify(add_json),
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			success: function (data) {
				console.log(data)
				$('#messageModal').find(".modal-title").text("success")
				$('#messageModal').find(".modal-body").html('<p>' + 'course added successfully' + '</p>')
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
		//var json_object = jQuery.parseJSON()		
		//console.log(add_json);
	}
	function CILO_dependencies_search() {
		var text = encodeURI($("#search-text").val())

		if ($("#search-type-switch").attr("value") == 1) {
			$.ajax({
				type: "GET",
				url: "/api/v1/search/cilo?search_type=cilo&keyword=" + text,
				async: false,
				dataType: "json",
				success: function (data) {
					if (data.cilos.length == 0) {
						$('#messageModal').find(".modal-title").text("message")
						$('#messageModal').find(".modal-body").html('<p>' + "There is no corresponding result" + '</p>')
						$('#messageModal').modal('show')
					} else {
						$(".define-box-result-table").find(".CLIOs-define-tr").remove()
						for (var i = 0; i < data.cilos.length; i++) {
							var append_text = '\
								<tr class="CLIOs-define-tr" style="text-align: center;">\
									<td class="CILO-ID-td" style="display: none;">'+ data.cilos[i].id + '</td>\
									<td class="course-name-td">'+ data.cilos[i].course_name + '</td>\
									<td class="CILO-description-td">'+ data.cilos[i].cilo_description + '</td>\
									<td class="CILOs-button-td"><button type="button" class="btn btn-light"\
											onclick="CILOs_define_page_add(this)">\
											<i class="fa fa-plus"></i>\
										</button></td>\
								</tr>'
							$("#define-box-result-table").append(append_text)
						}
					}
				},
				error: function (jqXHR) {
					$('#messageModal').find(".modal-title").text("error")
					$('#messageModal').find(".modal-body").html('<p>' + jqXHR.responseJSON.error + '</p>')
					$('#messageModal').modal('show')
				}
			})
		} else {
			$.ajax({
				type: "GET",
				url: "/api/v1/search/cilo?keyword=" + text,
				async: false,
				dataType: "json",
				success: function (data) {
					if (data.cilos.length == 0) {
						$('#messageModal').find(".modal-title").text("message")
						$('#messageModal').find(".modal-body").html('<p>' + "There is no corresponding result" + '</p>')
						$('#messageModal').modal('show')
					} else {
						$(".define-box-result-table").find(".CLIOs-define-tr").remove()
						for (var i = 0; i < data.cilos.length; i++) {
							var append_text = '\
								<tr class="CLIOs-define-tr" style="text-align: center;">\
									<td class="CILO-ID-td" style="display: none;">'+ data.cilos[i].id + '</td>\
									<td class="course-name-td">'+ data.cilos[i].course_name + '</td>\
									<td class="CILO-description-td">'+ data.cilos[i].cilo_description + '</td>\
									<td class="CILOs-button-td"><button type="button" class="btn btn-light"\
											onclick="CILOs_define_page_add(this)">\
											<i class="fa fa-plus"></i>\
										</button></td>\
								</tr>'
							$("#define-box-result-table").append(append_text)
						}
					}
				},
				error: function (jqXHR) {
					$('#messageModal').find(".modal-title").text("error")
					$('#messageModal').find(".modal-body").html('<p>' + jqXHR.responseJSON.error + '</p>')
					$('#messageModal').modal('show')
				}
			})
		}
	}