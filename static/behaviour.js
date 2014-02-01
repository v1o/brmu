jQuery(document).ready(function(){

	var results_template = "<div id='results_container' style='display: none;'>\
								<div style='margin: 2px;'><input type='search' class='search_field' placeholder='search this list'></input></div>\
								<div style='margin: 2px;' class='results'><table id='results_list'></table></div>\
								<div style='margin: 2px;'><button id='close_list' class='close_content'>Close</button></div>\
							</div>";

	jQuery("#select_city").click(function(){
		jQuery(".select").attr("disabled", "disabled");
		jQuery.get(
				'/cities',
				function(data){

					jQuery(results_template).insertAfter("#select_city");
					
					jQuery.each(data, function(k, v){
						jQuery("#results_list").append("<tr><td class='option'>"+v+"</td></tr>");
					});
					
					jQuery("#results_container").show('slow');
					
				}
			);
	});

	jQuery("#select_beer").click(function(){
		jQuery(".select").attr("disabled", "disabled");
		jQuery.get(
				'/beers',
				function(data){

					jQuery(results_template).insertAfter("#select_beer");
					
					jQuery.each(data, function(k, v){
						jQuery("#results_list").append("<tr><td class='option'>"+v+"</td></tr>");
					});
					
					jQuery("#results_container").show('slow');
					
				}
			);
	});

	jQuery("#select_place").click(function(){
		if (jQuery("#select_city").html() != "Select a city") {
			var value = jQuery("#select_city").html();
			jQuery(".select").attr("disabled", "disabled");
			jQuery.get(
					'/places',
					{
						data: value
					},
					function(response){
						if (response == "Not Found !"){
							alert(response);
							jQuery(".select").removeAttr("disabled");
						} else {
							jQuery(results_template).insertAfter("#select_place");
							
							jQuery.each(response, function(k, v){
								jQuery("#results_list").append("<tr><td class='option'>"+v+"</td></tr>");
							});
							
							jQuery("#results_container").show('slow');
						}
					}

				);
		} else {
			alert("Select a city !");
			jQuery(".select").removeAttr("disabled");
		}

	});		

	jQuery("#submit_search").click(function(){
		var city = jQuery("#select_city").html();
		var place = jQuery("#select_place").html();
		var beer = jQuery("#select_beer").html();
		var search = city+"_"+place+"_"+beer;
		if ((city == "Select a city") || (place == "Select a place") || (beer == "Select a beer")) {
			alert("Please select City&Place&Beer !");
		} else {
			jQuery.get(
				'/search',
				{
					data: search
				},
				function(response){
						if (response == "Not Found !"){
							alert(response);
						} else {
							alert ("Found !");
						}
					}
				);
		}
	});	

	jQuery("#add_place_beer").click(function(){
		var city = jQuery("#select_city").html();
		var place = jQuery("#enter_place").val();
		var beer = jQuery("#enter_beer").val();	
		var add_data = city+"_"+place+"_"+beer
		if ((city == "Select a city") || (place == "") || (beer == "")){
			alert("Please enter all information !");
		} else {
			jQuery.post(
				'/add',
				{
					data: add_data
				},
				function(response){
					alert(response);
					}
				);
		}	
	})

	//search
	$(document).on('keyup', ".search_field", function() {
 
        // Retrieve the input field text and reset the count to zero
        var filter = $(this).val(), count = 0;
 
        // Loop through the table rows
        $("table tr").each(function(){
 
            // If the list item does not contain the text phrase fade it out
            if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                $(this).hide();
 
            // Show the list item if the phrase matches
            } else {
                $(this).show();
            }
        });

    });	

	jQuery(document).on("click", ".option", function(){
		var value = jQuery(this).html();
		jQuery("results_container").hide('slow');
		jQuery(".select").removeAttr('disabled');
		jQuery("#results_container").prev().html(value);
		jQuery("#results_container").remove();
	});

	jQuery(document).on("click" , "#close_list", function(){
		jQuery("#results_container").remove();
		jQuery(".select").removeAttr("disabled");  
	});

	jQuery("#show_add_page").click(function(){
		jQuery("#search_page").hide();
		jQuery("#add_page").show('slow');
	});

	jQuery("#show_search_page").click(function(){
		jQuery("#add_page").hide();
		jQuery("#search_page").show('slow');
	});		

	jQuery("#enter_place").click(function(){
		jQuery(this).val("");
	});

	jQuery("#enter_beer").click(function(){
		jQuery(this).val("");
	});			
});