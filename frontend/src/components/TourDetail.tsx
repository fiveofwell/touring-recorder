import { Link, useNavigate } from 'react-router-dom';
import type { TourLinkProps, TourDetailProps } from '../types/types';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';

export const TourLink = ({ client_tour_id, tour_name }: TourLinkProps) => (
	<Link to={`/tours/${client_tour_id}/points`} className="tour-detail">
		{tour_name}
	</Link>
);

export const TourDetail = ({
	client_tour_id,
	tour_name,
	device_name,
	created_at,
	updated_at,
	onDelete,
}: TourDetailProps) => {
	const navigate = useNavigate();

	const deleteTour = async () => {
		if (!confirm('本当にこのツーリングの履歴を削除しますか？')) {
			return;
		}

		try {
			await apiFetch(`/api/internal/tours/${client_tour_id}`, {
				method: 'DELETE',
			});
			onDelete(client_tour_id);
		} catch (error) {
			if (error instanceof UnauthorizedError) return;
			console.error('ツーリングの削除に失敗しました: ', error);
			alert('ツーリングの削除に失敗しました。再度お試しください。');
		}
	};

	return (
		<li>
			<TourLink client_tour_id={client_tour_id} tour_name={tour_name} />
			<p>Client tour id: {client_tour_id}</p>
			{device_name && <p>Device name: {device_name}</p>}
			<p>Created at: {created_at.toLocaleString('ja-JP')}</p>
			<p>Updated at: {updated_at.toLocaleString('ja-JP')}</p>
			<button onClick={deleteTour}>ツーリングを削除する</button>
			<button onClick={() => navigate(`/tours/${client_tour_id}/edit`)}>
				ツーリングの名前を変更する
			</button>
			<hr />
		</li>
	);
};
