function formatDate(iso) {
  if (!iso) return "-";
  return new Date(iso + "Z").toLocaleString("ja-JP");
}


async function getTours() {
	const url = `/api/internal/tours`;

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
			<a class="tour-detail" href="./view-tour.html?tour_id=${encodeURIComponent(tour.tour_id)}">${tour.tour_name}</a>
			<ul>
				<li>
					<p>tour id: ${tour.tour_id}</p>
				</li>
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
		`;

		const deleteButton = document.createElement("button");
		deleteButton.textContent = "このツーリングの履歴を削除";
		deleteButton.addEventListener("click", () => {
			deleteTour(tour.tour_id);
		});

		const nameChangeButton = document.createElement("button");
		nameChangeButton.textContent = "このツ-リングの名前を変更";
		nameChangeButton.addEventListener("click", () => {
			const url = "./change-tour-name.html?tour_id=" + encodeURIComponent(tour.tour_id)
			window.location.href = url

		});

		li.appendChild(nameChangeButton)
		li.appendChild(deleteButton)

		li.appendChild(document.createElement('hr'))

		list.appendChild(li)
	}
}


async function deleteTour(tour_id) {
	if (!confirm("本当にこのツーリングの履歴を削除しますか？")) {
		return;
	}

	const url = `/api/internal/tours/${tour_id}`;

	try {
		const response = await fetch(
			url, {
				method: "DELETE",
			}
		);
	
		if (!response.ok) {
			throw new Error(`HTTP ${response.status} ${response.statusText}`);
		}

		location.reload();
	} catch (error) {
		console.error('エラーが発生しました', error);
		showError(error);
	}
	return;
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
