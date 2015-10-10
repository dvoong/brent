var properties = [
    {
	name: "property1",
	postcode: "HA0 1AA",
	type: "terrace",
	sensors: [
	    {
		id: 0,
		location: "Living Room",
		measurements: [
		    {
			datetime: '2015-10-09 10:47:01.482559',
			temp: 20.112,
			humidity: 50,
			lux: 2386,
		    },
		    {
			datetime: '2015-10-09 11:47:01.482559',
			temp: 22.112,
			humidity: 58,
			lux: 2786,
		    },
		    {
			datetime: '2015-10-09 13:47:01.482559',
			temp: 23.192,
			humidity: 57,
			lux: 3386,
		    },
		]
	    },
	    {
		id: 1,
		location: "Kitchen",
		measurements: [
		    {
			datetime: '2015-10-09 12:47:01.482559',
			temp: 24.192,
			humidity: 52,
			lux: 2886,
		    },

		],
	    }
	]
    },
    {
	name: "property2",
	postcode: "HA0 1AB",
	type: "semi-detached",
	sensors: [],
    },
    {
	name: "property3",
	postcode: "HA0 1AN",
	type: "flat",
	sensors: [],
    },
]

$(document).ready(function(){
    var property_details = $("#property-details");
    var rows = property_details.find("tr")
    console.log(rows);
    var name_row = $(rows[0]);
    var postcode_row = $(rows[1]);
    var type_row = $(rows[2]);

    $("#properties .btn-group .btn").click(function(){
	var property;
	for(i=0; i<properties.length; i++){
	    if(properties[i].name == $(this).find("input").attr("id")){
		property = properties[i];
		break;
	    }
	}

	name_row.find("td").last().html(property.name);
	postcode_row.find("td").last().html(property.postcode);
	type_row.find("td").last().html(property.type);
    });

    $("#properties .btn-group .btn").first().click();

    var m = [20, 20, 30, 50],
	w = 960 - m[1] - m[3],
	h = 500 - m[0] - m[2],
	barPadding = 1;
    
    
    var svg = d3.select("#graphs").append("svg")
        .attr("width", w + m[1] + m[3])
        .attr("height", h + m[0] + m[2])
	.append("g")
        .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    var sensor = properties[0].sensors[0];
    var measurements = sensor.measurements;

    console.log(sensor);
    console.log(measurements);

    for(i=0; i<measurements.length; i++){
	var date = new Date(measurements[i].datetime);
	console.log(date);
    }

    console.log("Random Number: " + Math.random());

    for(i=0; i<measurements.length; i++){
	measurements[i].datetime = new Date(measurements[i].datetime);
    }

    var minDate = d3.min(measurements, function(d){
	return d.datetime;
    });

    var maxDate = d3.max(measurements, function(d){
	return d.datetime;
    });

    console.log(measurements);
    console.log(minDate);
    console.log(maxDate);
    
    var xscale = d3.time.scale().range([0, w]).domain([minDate, maxDate]);
    var xaxis = d3.svg.axis();
    xaxis.orient('bottom');
    xaxis.scale(xscale);
    // xaxis.ticks(d3.time.minutes, 30)
    // xaxis.ticks(measurements.length);
    // xaxis.tickFormat(d3.time.format('%Y-%m-%d %H:%M'))
    svg.append("g")
	.call(xaxis)
	.attr("transform", "translate(0, " + h + ")");

    var minTemp = d3.min(measurements, function(d){return d.temp;})
    minTemp = minTemp - 0.1 * minTemp;
    console.log(minTemp);
    var maxTemp = d3.max(measurements, function(d){return d.temp;})
    maxTemp = maxTemp + 0.1 * maxTemp;
    console.log(maxTemp);
    var yscale = d3.scale.linear()
	.range([h, 0])
	.domain([minTemp, maxTemp]);
    var yaxis = d3.svg.axis();
    yaxis.scale(yscale);
    yaxis.orient('left');
    svg.append("g").call(yaxis);
    
    svg.selectAll('rect')
	.data(measurements)
	.enter()
	.append("rect")
	.attr({
	    x: function(d, i){return i * (w / measurements.length);},
	    y: function(d){ return yscale(d.temp); },
	    width: w / measurements.length - barPadding,
	    height: function(d){ return h - yscale(d.temp); },
	});

    svg.selectAll("text")
	.data(measurements)
	.enter()
	.append("text")
	.text(function(d){ return d.temp; })
	.attr({
	    x: function(d, i){return (i + 0.5) * (w / measurements.length);},
	    y: function(d){ return h - d.temp; },
	    "text-anchor": "middle",
	});

});
