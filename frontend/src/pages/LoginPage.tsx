import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
	const navigate = useNavigate();
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const [isSubmitting, setIsSubmitting] = useState(false);

	const handleSubmit = async (event: React.SubmitEvent<HTMLFormElement>) => {
		event.preventDefault();

		if (!username.trim() || !password) {
			setError('ユーザー名とパスワードを入力してください。');
			return;
		}

		setError('');
		setIsSubmitting(true);

		try {
			const response = await fetch('/token', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				body: new URLSearchParams({
					username: username.trim(),
					password,
				}).toString(),
			});

			if (!response.ok) {
				throw new Error('ログインに失敗しました');
			}

			const token = (await response.json()) as {
				access_token: string;
				token_type: string;
			};

			localStorage.setItem('access_token', token.access_token);
			localStorage.setItem('token_type', token.token_type);
			navigate('/tours');
		} catch (err) {
			setError(err instanceof Error ? err.message : 'ログインに失敗しました。');
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<form onSubmit={handleSubmit}>
			<h1>ログイン</h1>
			{error && (
				<p style={{ color: 'red' }} role="alert">
					{error}
				</p>
			)}
			<label>
				ユーザー名
				<input
					type="text"
					value={username}
					required
					autoComplete="username"
					onChange={(event) => setUsername(event.target.value)}
				/>
			</label>
			<label>
				パスワード
				<input
					type="password"
					value={password}
					required
					autoComplete="current-password"
					onChange={(event) => setPassword(event.target.value)}
				/>
			</label>
			<button type="submit" disabled={isSubmitting}>
				{isSubmitting ? 'ログイン中...' : 'ログイン'}
			</button>
		</form>
	);
};

export default LoginPage;
