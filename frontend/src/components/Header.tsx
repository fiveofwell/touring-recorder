import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';

export const Header = () => {
	const navigate = useNavigate();
	const [isLoggingOut, setIsLoggingOut] = useState(false);

	const handleLogout = async () => {
		setIsLoggingOut(true);
		try {
			await apiFetch('/token', {
				method: 'DELETE',
			});
		} catch (error) {
			if (error instanceof UnauthorizedError) return;
			console.error('サーバーとの同期に失敗しました: ', error);
		} finally {
			localStorage.removeItem('access_token');
			setIsLoggingOut(false);
			navigate('/');
		}
	};

	return (
		<header>
			<h1>Touring Recorder</h1>
			<nav>
				<Link to="/tours">ツーリング一覧</Link>
				<Link to="/devices">デバイス管理</Link>
				<button onClick={handleLogout} disabled={isLoggingOut}>
					{isLoggingOut ? 'ログアウト中...' : 'ログアウト'}
				</button>
			</nav>
		</header>
	);
};
