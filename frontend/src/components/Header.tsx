import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';

export const Header = () => {
	const navigate = useNavigate();
	const [isLoggingOut, setIsLoggingOut] = useState(false);

	const handleLogout = async () => {
		setIsLoggingOut(true);
		try {
			const response = await fetch('/token', {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${localStorage.getItem('access_token')}`,
				},
			});

			if (!response.ok) {
				throw new Error('サーバーとの同期に失敗しました');
			}
		} catch (err) {
			console.error(
				err instanceof Error ? err.message : 'ログアウトに失敗しました。',
			);
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
