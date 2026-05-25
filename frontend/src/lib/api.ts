import { UnauthorizedError } from './errors';

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
		console.error('Unauthorized: アクセストークンが無効または期限切れです。');
		alert('再度ログインしてください。');
		window.location.href = '/';
		throw new UnauthorizedError();
	}

	if (!response.ok) {
		throw new Error(`HTTP Error: ${response.status}`);
	}

	return response;
};
