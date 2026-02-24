function formatDate(iso) {
  if (!iso) return "-";
  return new Date(iso + "Z").toLocaleString("ja-JP");
}


function getTourId() {
	const url = new URL(window.location.href);
	return url.searchParams.get("tour_id");
}


async function getPoints() {
	const tour_id = getTourId();
	if (!tour_id) {
		showMessage("tour_idが指定されていません");
		return;
	}

	showMessage("読み込み中・・・");

	try {
		const url = `/api/internal/tours/${encodeURIComponent(tour_id)}`;
		const response = await fetch(
			url,
			{
				method: "GET",
				headers: {
					Accept: "application/json",
				},
			}
		)
	
		if (!response.ok) {
			throw new Error(`HTTP ${response.status} ${response.statusText}`);
		}
	
		const json_response = await response.json();
		hideMessage();
		make_map(json_response)
	} catch (error) {
		console.error('エラーが発生しました', error);
		showError(error);
	}
}


function make_map(response) {
	const points = response.points;
	if (!points || points.length === 0){
		showMessage("ポイントがありません")
		return;
	}

	if (!map) {
		map = L.map('map')
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '© OpenStreetMap contributors'
		}).addTo(map);
	}


	const latlngs = [];
	for (const point of points) {
		latlngs.push([point.latitude, point.longitude])
	}

	if (startMarker && map.hasLayer(startMarker)) {
		map.removeLayer(startMarker);
	}
	if (endMarker && map.hasLayer(endMarker)) {
		map.removeLayer(endMarker);
	}

	startMarker = L.marker([points[points.length - 1].latitude, points[points.length - 1].longitude]).addTo(map);
	startMarker.bindPopup("ツーリング開始: " + formatDate(points[points.length - 1].timestamp))
	startMarker.openPopup();

	endMarker = L.marker([points[0].latitude, points[0].longitude]).addTo(map);
	endMarker.bindPopup("ツーリング終了: " + formatDate(points[0].timestamp))
	if (polyline && map.hasLayer(polyline)) {
		map.removeLayer(polyline);
	}

	polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
	map.fitBounds(polyline.getBounds());
}


function showError(error) {
	console.error(error);
	const div = document.getElementById('mapStatus');
	div.innerHTML = "エラーが発生しました";
}


function showMessage(message) {
	const div = document.getElementById('mapStatus');
	div.innerHTML = message;
}


function hideMessage() {
	const div = document.getElementById('mapStatus');
	div.innerHTML = "";
}


let map;
let polyline;
let startMarker;
let endMarker;

getPoints();
