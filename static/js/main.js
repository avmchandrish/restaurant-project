const search = document.getElementById('search');
const suggest = document.getElementById('suggestions');
const dropdown = document.getElementsByClassName('card')
const btn = document.getElementById('download-btn')
var latlong_global="";
var lat="";
var long="";
var match_global="";
var restList="";

// Call the swiggy api and show the values of suggestions
async function searchAddress(searchText){
	const url = "http://127.0.0.1:5000/search?input=".concat(searchText)
	const res = await fetch(url);
	const matches = await res.json();

	if (searchText.length===0){
		matches.data=[];
		suggest.innerHTML = '';
	};

	match_global=matches;
	outputHtml(matches);
	console.log(matches);
	document.querySelectorAll('.card').forEach((item, index) => {
  		item.addEventListener('click', function() {click(item, index)} ,false)
	});
};

// Show the matches in the webpage
function outputHtml(matches){
	if(matches.data.length > 0){
		const html = matches.data.map(match => `
			<div class= "card card-body mb-1">
				<h4>${match.description}</h4>

			</div>


			`).join("");
		suggest.innerHTML = html;
	}
}

// Once an address is selected, getting the lat and long
function click(item, index){
	search.value = item.innerText;
	console.log(index);
	placeid = match_global.data[index].place_id;
	suggest.innerHTML = '';
	console.log(placeid);
	getLatlong(placeid);
}

async function getLatlong(placeid){
	const api = "http://127.0.0.1:5000/geocode?placeid=" + placeid;
	const res = await fetch(api);
	const latlongJson = await res.json();
	lat = latlongJson.data[0].geometry.location.lat
	long = latlongJson.data[0].geometry.location.lng
	latlong_global=latlongJson;
	console.log(latlongJson);
}

async function download(){
	// First Step: Get the number of restaurants in the listing
	const api = "http://127.0.0.1:5000/restaurants?lat=" + lat + "&long=" + long + "&offset=0";
	const res = await fetch(api);
	JsonArray = await res.json();
	console.log(JsonArray)
	restList = JsonArray
	// defining the column list, for first row
	columns = ['name', 'rest_id', 'city', 'area', 'rating', 'cuisine', 'cost_for_two', 'del_time', 'max_del_time', 'min_del_time', 
         'loc', 'disc_meta', 'disc_type', 'disc_op_type', 'fee', 'menu_link', 'slug']

    JsonFields = ['name', 'rest_id', 'city', 'area', 'rating', 'cuisine', 'cost_for_two', 'del_time','loc', 'disc_meta', 'disc_type','menu_link']

    //code for converting the json into a csv
    var csvStr = JsonFields.join(",") + "\n";

    JsonArray.forEach(element => {
        name = '"' + element.name + '"';
        rest_id = '"' + element.rest_id + '"';
        city = '"' + element.city + '"';
        area = '"' + element.area + '"';
        rating = '"' + element.rating + '"';
        cuisine = '"' + element.cuisine + '"';
        cost_for_two = '"' + element.cost_for_two + '"' ;
        del_time = '"' + element.del_time + '"';
        loc = '"' + element.loc + '"';
        disc_meta = '"' + element.disc_meta + '"';
        disc_type = '"' + element.disc_type + '"' ;
        menu_link = '"' + element.menu_link + '"' ;

        csvStr += name + ',' + rest_id + ','  + city + ',' + area + ',' + rating + ',' + cuisine + ',' + cost_for_two + ',' + del_time +
         ',' + loc + ',' + disc_meta + ',' + disc_type + ',' + menu_link + "\n";
        })


    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvStr);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'output.csv';
    hiddenElement.click();
}



search.addEventListener('input', function(){searchAddress(search.value)}, false);
btn.addEventListener('click', download, false);

