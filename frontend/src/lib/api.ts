export const apiFetch = async (path: string, options: RequestInit = {}) => {
	const token = localStorage.getItem('access_token');

	const response = await fetch(path, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`,
			...options.headers,
		},
	});

	if (response.status === 401) {
		localStorage.removeItem('access_token');
		window.location.href = '/';
	}

	if (!response.ok) {
		throw new Error(`HTTP Error: ${response.status}`);
	}

	return response;
};
