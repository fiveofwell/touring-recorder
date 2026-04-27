import { Link } from 'react-router-dom';

export const Header = () => {
	return (
		<header>
			<h1>Touring Recorder</h1>
			<nav>
				<Link to="/tours">ツーリング一覧</Link>
				<Link to="/devices">デバイス管理</Link>
				<Link to="/" onClick={() => localStorage.removeItem('access_token')}>
					ログアウト
				</Link>
			</nav>
		</header>
	);
};
