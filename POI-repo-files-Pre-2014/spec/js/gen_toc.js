$( document ).ready(function() {
	
	// Auto number the annexes (must have class="autoannex" )
	// Must do this first so that the Annexes will be listed with their auto numbering
	var myArray = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ];
	$(".autoannex").each( function() {
		var val = myArray[ 0 ];
		$(this).prepend(val);
	// set id of parent <h1> to the auto number 	
		$(this).parent("h1").attr( "id", val );
		myArray.shift(); 
	});
	
	// Now run the TOC Generator
	var toc_counter = 0;	
	var ToC =
	  "<nav role='navigation' id='toc' class='table-of-contents'>"
		+ "<header>"
		+ "<p class='prefacehead'>Table of Contents</p>"
		+ "</header>"
		+ "<dir><ul>";
	var newLine, el, title, link, last;
	$("section :header").each(function() {
		if ($(this).is("h1")) {
			while( last > 1 ){
				ToC += "</ul>";
				last = last - 1;
			}
			last = "1";
		} else if ($(this).is("h2")) {
			if (last < 2) { 
				ToC += "<ul>";
			}	
			while( last > 2 ){
				ToC += "</ul>";
				last = last - 1;
			}
			last = "2";
		} else if ($(this).is("h3")) {
			if (last < 3) {
				ToC += "<ul>";
			}
			while( last > 3 ){
				ToC += "</ul>";
				last = last - 1;
			}
			last = "3";
		} else if ($(this).is("h4")) {
			if (last < 4) {
				ToC += "<ul>";
			}
			while( last > 4 ){
				ToC += "</ul>";
				last = last - 1;
			}
			last = "4";
		} else if ($(this).is("h5")) {
			if (last < 5) { ToC += "<ul>"; }
			while( last > 5 ){ ToC += "</ul>"; last = last - 1; }
			last = "5";
		} else if ($(this).is("h6")) {
			if (last < 6) { ToC += "<ul>"; }
			last = "6";
		}
		el = $(this);
		title = el.text();
		if (el.attr("id")) {
			link = "#" + el.attr("id");				
		} else {
			toc_counter++;
			link = "#" + toc_counter;
		}
		newLine =
			"<li>" +
			"<a href='" + link + "'>" +
			title +
			"</a>" +
			"</li>";
		ToC += newLine;
	}); 
	ToC +=
		"</ul></dir>" +
		"</nav>";
	$(".all-headings").prepend(ToC);
});