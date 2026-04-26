import { Link, useNavigate } from 'react-router-dom';
import type { TourLinkProps, TourDetailProps } from '../types/types';

export const TourLink = ({ id, name }: TourLinkProps) => (
	<Link to={`/tours/${id}`} className="tour-detail">
		{name}
	</Link>
);

export const TourDetail = ({
	tour_id,
	tour_name,
	device_id,
	started_at,
	last_seen_at,
	onDelete,
}: TourDetailProps) => {
	const navigate = useNavigate();

	const deleteTour = async () => {
		if (!confirm('本当にこのツーリングの履歴を削除しますか？')) {
			return;
		}

		try {
			const response = await fetch(`/api/internal/tours/${tour_id}`, {
				method: 'DELETE',
			});
			if (!response.ok) {
				throw new Error('APIエラー');
			}
			onDelete(tour_id);
		} catch (error) {
			console.error(error);
			alert('削除に失敗しました');
		}
	};

	return (
		<li>
			<TourLink id={tour_id} name={tour_name} />
			<p>Tour id: {tour_id}</p>
			<p>Device id: {device_id}</p>
			<p>Started at: {started_at.toLocaleString('ja-JP')}</p>
			<p>Last seen at: {last_seen_at.toLocaleString('ja-JP')}</p>
			<button onClick={deleteTour}>ツーリングを削除する</button>
			<button onClick={() => navigate(`/tours/${tour_id}/name-change`)}>
				ツーリングの名前を変更する
			</button>
			<hr />
		</li>
	);
};
