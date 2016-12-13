$(function(){
	rie_rows = $("#rie-container").children(".rie-row")

	counter = 1

	$.each(rie_rows, function(i, rie_row){
		$(rie_row).attr("id", "rie_"+(i+1))
		counter++
	})

	$.each($(".rie-del"), function(i, btn){
		$(btn).click(function(){
			id = "#rie_"+(i+1)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_ries()
			})
		})
	})

	function check_ries(){
		if($("#rie-container").children(".rie-row").length < 1)
			$("#no-ries").removeClass("hide")
		else
			if(!($("#no-ries").hasClass("hide")))
				$("#no-ries").addClass("hide")
			
	}

	$("#add-rie-btn").click(function(){
		$("#rie-container").append(
			"<div id='rie_"+counter+"' class='row rie-row'>"+
				"<div class='col s10'>"+
					"<input name='texto_rie' type='text' placeholder='Riesgo' class='validate'>"+
				"</div>"+
				"<div class='col s2'>"+
					"<button type='button' class='rie-del btn-floating waves-effect waves-light red lighten-2'><i class='material-icons'>delete</i></button>"+
				"</div>"+
			"</div>"
		)
		var id = "#rie_"+counter
		counter++
		$(id).find(".rie-del").click(function(){
			console.log("click "+id)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_ries()
			})
		})
		check_ries()
	})

})