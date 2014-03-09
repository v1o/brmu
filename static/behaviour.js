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
						jQuery("#results_list").append("<tr><td class='option' >"+v+"</td></tr>");
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
							alert("No places available for the selected City :(");
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

	//general search
	jQuery("#submit_search").click(function(){
		var city = jQuery("#select_city").html();
		var place = jQuery("#select_place").html();
		var beer = jQuery("#select_beer").html();
		if (city == "Select a city") {
			alert("Please select City");
		} else {
			if ((place == "Select a place") && (beer == "Select a beer")){
				alert("Please select a beer / place or both");
			} else {
				var search_criteria = city+"_"+place+"_"+beer;
				//alert(search_criteria);
				jQuery.get(
					'/search',
					{
						data: search_criteria
					},
					function(response){
						if (response == "Not Found !"){
							alert(response);
						} else {
							//console.log(response.size);
							jQuery("#search_results").append("<div id='results_wrapper'></div>");
							jQuery.each(response, function(k, v){
								console.log(k);
								jQuery("#results_wrapper").append(k);
								jQuery("#results_wrapper").append("<table id='table_results'></table");
								//console.log(v);
								jQuery.each(v, function(kk, vv){
									jQuery("#table_results").append("<tr><td>"+kk+"</td><td>Price</td><td>"+vv.price+"</td></tr>");
								});
							});
							jQuery("#search_results").dialog({
								close: function(){
									jQuery("#results_wrapper").remove();
								}
							});

						}
					}
					);
			}
		}
		
	});

	jQuery("#add_place_beer").click(function(){
		var city = jQuery("#select_city").html();
		var place = jQuery("#enter_place").val();
		var beer = jQuery("#enter_beer").val();	
		var beer_type = jQuery("#beer_type").val();
		var beer_price = jQuery("#enter_beer_price").val();

		var date = new Date();
		var day = date.getDate();
		var month = date.getMonth()+1;
		var year = date.getFullYear();
		var hour = date.getHours();
		var minute = date.getMinutes();
		var second = date.getSeconds();
		var submit_date = day+"-"+month+"-"+year+"_"+hour+":"+minute+":"+second;

		var add_data = city+"_places_beers"+";"+place+"-"+beer+";"+beer_type+";"+beer_price+";"+submit_date+";";
		console.log(add_data);
		
		if ((city == "Select a city") || (place == "") || (beer == "") || (beer_price == "") || (beer_type == "Select beer type")){
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

	jQuery("#switch_page").click(function(){
		if (jQuery("#search_page").is(':visible')) {
			jQuery("#search_page").hide();
			jQuery(this).removeClass("add_page_icon");
			jQuery(this).addClass("search_page_icon");
			jQuery(this).html("Go to Search page");
			jQuery("#add_page").show('slow');
		} else {
			jQuery("#add_page").hide();
			jQuery(this).removeClass("search_page_icon");
			jQuery(this).addClass("add_page_icon");			
			jQuery(this).html("Go to Add page");
			jQuery("#search_page").show('slow');
		}
	});

	jQuery("#enter_place").click(function(){
		jQuery(this).val("");
	});

	jQuery("#enter_beer").click(function(){
		jQuery(this).val("");
	});			

	jQuery("#enter_beer_price").click(function(){
		jQuery(this).val("");
	});

	jQuery("#feedback_button").click(function(){
		jQuery("#feedback_section").show('slow');
	});

	jQuery("#send_feedback").click(function(){
		var feedback_text = jQuery("#enter_feedback").val();
		jQuery.post(
				'/add_feedback',
				{
					data: feedback_text
				},
				function(response){
					alert("Feedback sent !");
				}
			);
		jQuery("#enter_feedback").val('');
		jQuery("#feedback_section").hide('slow');
	});

	jQuery("#cancel_send_feedback").click(function(){
		jQuery("#feedback_section").hide('slow');		
	});
});