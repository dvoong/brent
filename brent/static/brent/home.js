// var properties = [
//     {
// 	name: "property1",
// 	postcode: "HA0 1AA",
// 	type: "terrace",
// 	sensors: [
// 	    {
// 		id: 0,
// 		location: "Living Room",
// 		measurements: [
// 		    {
// 			datetime: '2015-10-09 10:47:01.482559',
// 			temperature: 20.112,
// 			humidity: 50,
// 			lux: 2386,
// 		    },
// 		    {
// 			datetime: '2015-10-09 11:47:01.482559',
// 			temperature: 22.112,
// 			humidity: 58,
// 			lux: 2786,
// 		    },
// 		    {
// 			datetime: '2015-10-09 13:47:01.482559',
// 			temperature: 23.192,
// 			// humidity: 57,
// 			lux: 3386,
// 		    },
// 		]
// 	    },
// 	    {
// 		id: 1,
// 		location: "Kitchen",
// 		measurements: [
// 		    {
// 			datetime: '2015-10-09 12:47:01.482559',
// 			temp: 24.192,
// 			humidity: 52,
// 			lux: 2886,
// 		    },

// 		],
// 	    }
// 	]
//     },
//     {
// 	name: "property2",
// 	postcode: "HA0 1AB",
// 	type: "semi-detached",
// 	sensors: [
// 	    {
// 		id: 0,
// 		location: "Kitchen",
// 		measurements: [],
// 	    }
// 	],
//     },
//     {
// 	name: "property3",
// 	postcode: "HA0 1AN",
// 	type: "flat",
// 	sensors: [
// 	    {
// 		id: 0,
// 		location: "Downstairs Corridor",
// 		measurements: [],
// 	    }
// 	],
//     },
// ]

$(document).ready(function(){
    var property;
    var property_details = $("#property-details");
    var rows = property_details.find("tr")
    var name_row = $(rows[0]);
    var postcode_row = $(rows[1]);
    var type_row = $(rows[2]);
    var varButton = $("#graph-var-selector button");
    var sensorSelector = $("#graph-sensor-selector");

    for(i=0; i<properties.length; i++){
	var sensors = properties[i].sensors
	for(j=0; j<sensors.length; j++){
	    var measurements = sensors[j].measurements;
	    for(k=0; k<measurements.length; k++){
		var date = new Date(measurements[k].datetime);
		measurements[k].datetime = date;
	    }
	}
    }

    console.log(properties);
    
    var m = [20, 20, 30, 50],
	w = 960 - m[1] - m[3],
	h = 500 - m[0] - m[2],
	barPadding = 1;
    
    var svg = d3.select("#graphs").append("svg")
        .attr("width", w + m[1] + m[3])
        .attr("height", h + m[0] + m[2])
	.append("g")
        .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    $("#properties .btn-group .btn").click(function(){
	console.log("properties:");
	console.log(properties);
	for(i=0; i<properties.length; i++){
	    if(properties[i].name == $(this).find("input").attr("id")){
		property = properties[i];
		break;
	    }
	}

	name_row.find("td").last().html(property.name);
	postcode_row.find("td").last().html(property.postcode);
	type_row.find("td").last().html(property.type);
	listSensors();
	refreshGraph();
    });

    $("#properties .btn-group .btn").first().click();

    $(".var-select").click(function(){
	varButton.text($(this).text());
	refreshGraph();
    });
    
    // $("#temp-select").click(function(){
    // 	if(varButton.html() != "Temperature"){
    // 	    console.log("select temp");
    // 	    varButton.html("Temperature");
    // 	    refreshGraph();
    // 	}
    // });

    // $("#humidity-select").click(function(){
    // 	if(varButton.html() != "Humidity"){
    // 	    console.log("select humidity");
    // 	    varButton.html("Humidity");
    // 	    refreshGraph();
    // 	}
    // });

    function refreshGraph(){
	console.log("refreshGraph");

	// $(svg).empty();
	$(svg[0]).empty();
	
	var varName = $.trim(varButton.text());
	var sensor;
	for(i=0; i<property.sensors.length; i++){
	    if(property.sensors[i].id == sensorSelector.find("button").text()){
		sensor = property.sensors[i];
		break;
	    }
	}
	// var sensor = property.sensors[0] // TODO: Need a sensor selector
	console.log("sensor");
	console.log(sensor);
	var measurements = sensor.measurements;
	console.log(sensor.measurments);

	console.log(varName);
	
	var dataset = []
	for(i=0; i<measurements.length; i++){
	    var propertyName;
	    if(varName == "Temperature"){
		propertyName = "temperature";
	    } else if (varName == "Humidity"){
		propertyName = "relative_humidity";
	    } else if (varName == "Light"){
		propertyName = "light";
	    } else if (varName == "Vacancy"){
		propertyName  = "vacancy";
	    }
	    
	    if(measurements[i].hasOwnProperty(propertyName)){
		datum = {
		    datetime: measurements[i].datetime,
		    val: measurements[i][propertyName],
		}
	    dataset.push(datum);
	    }
	}

	console.log(dataset);

	var minDate = d3.min(dataset, function(d){
	    return d.datetime;
	});
	
	var maxDate = d3.max(dataset, function(d){
	    return d.datetime;
	});
	
	console.log(measurements);
	console.log(minDate);
	console.log(maxDate);
	
	var xscale = d3.time.scale().range([0, w]).domain([new Date(minDate - 3600 * 1000), new Date(maxDate.getTime() + (3600 * 1000))]);
	var xaxis = d3.svg.axis();
	xaxis.orient('bottom');
	xaxis.scale(xscale);
	// xaxis.ticks(d3.time.minutes, 30)
	// xaxis.ticks(measurements.length);
	// xaxis.tickFormat(d3.time.format('%Y-%m-%d %H:%M'))
	// svg.append("g")
	// 	.call(xaxis)
	// 	.attr("transform", "translate(0, " + h + ")");

	var minY = d3.min(dataset, function(d){ return d.val; });
	var maxY = d3.max(dataset, function(d){ return d.val; });
	console.log(minY);
	console.log(maxY);
	
	var yscale = d3.scale.linear()
	    .range([h, 0])
	    .domain([minY - minY * 0.1, maxY + maxY * 0.1]);
	var yaxis = d3.svg.axis();
	yaxis.scale(yscale);
	yaxis.orient('left');
	    
	
	// svg.selectAll("text")
    	//     .data(dataset)
    	//     .enter()
    	//     .append("text")
    	//     .text(function(d){ return d.val; })
    	//     .attr({
    	// 	x: function(d, i){ return xscale(d.datetime);},
    	// 	y: function(d){ return yscale(d.val); },
    	// 	"text-anchor": "middle",
    	//     });
	
	var line = d3.svg.line()
    	    .x(function(d){ return xscale(d.datetime); })
    	    .y(function(d){ return yscale(d.val); })
	
	
	svg.append("path")
            .datum(dataset)
            .attr("class", "line")
            .attr("d", line);
	
	svg.append("g").call(xaxis)
    	    .attr("transform", "translate(0, " + h + ")")
	    .attr("class", "axis");
	svg.append("g").call(yaxis)
	    .attr("class", "axis");

    }

    function listSensors(){
	console.log("listSensors");
	var sensorDropdownList = sensorSelector.find("ul");
	var sensorDropdownButton = sensorSelector.find("button");
	sensorDropdownList.empty()
	var sensors = property.sensors;
	for(i=0; i<sensors.length; i++){
	    if(i == 0){
		sensorDropdownButton.text(sensors[i].id);
	    }
	    sensorDropdownList.append("<li>" + sensors[i].id + "</li>");
	}
    };

    // $("#graph-sensor-selector").click(function(){
    // 	console.log("#graph-sensor-selector click");
    // });
    
    // $("#graph-sensor-selector ul").click(function(){
    // 	console.log("#graph-sensor-selector ul click");
    // });
    
    // $("#graph-sensor-selector ul li").click(function(){
    // 	console.log("#graph-sensor-selector ul li click");
    // });
    
    $("#graph-sensor-selector ul li").click(function(){
	console.log("test");
	// console.log($(this));
	// console.log($(this).html());
	// $("#graph-sensor-selector button").html($(this).html());
	$("#graph-sensor-selector button").text($.trim($(this).text()));
	refreshGraph();
    });

});

