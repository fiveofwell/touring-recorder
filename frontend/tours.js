import { API_BASE_URL } from "./settings.js"

function formatDate(iso) {
  if (!iso) return "-";
  return new Date(iso).toLocaleString();
}


async function getTours() {
	const url = `${API_BASE_URL}/tours`;

	showLoading()

	try {
		const response = await fetch(
			url, {
				method: "GET",
				headers: {
					Accept: "application/json",
					"Content-Type": "application/json",
				},
			}
		);
	
		if (!response.ok) {
			throw new Error(`HTTP ${response.status} ${response.statusText}`);
		}

		const tours = await response.json();
		showTours(tours)

	} catch (error) {
		console.error('エラーが発生しました', error);
		showError(error);
	}
}


function showTours(tours) {
	const list = document.getElementById('list');
	list.innerHTML = "";
	if (!Array.isArray(tours) || tours.length === 0) {
		list.innerHTML = "<li>ツーリングがありません</li>"
		return;
	}

	for (const tour of tours) {
		const li = document.createElement('li');
		li.innerHTML = `
			<a href="./view-tour.html?tour_id=${encodeURIComponent(tour.tour_id)}">${tour.tour_id}</a>
			<ul>
				<li>
					<p>device id: ${tour.device_id}</p>
				</li>
				<li>
					<p>started at: ${formatDate(tour.started_at)}</p>
				</li>
				<li>
					<p>Last seen at: ${formatDate(tour.last_seen_at)}</p>
				</li>
			</ul>
		`

		list.appendChild(li)
	}
}


function showError(error) {
	console.error(error);
	const list = document.getElementById('list');
	list.innerHTML = `<li>エラーが発生しました</li>`;
}


function showLoading() {
	const list = document.getElementById('list');
	list.innerHTML = `<li>読み込み中・・・</li>`;
}


getTours()
