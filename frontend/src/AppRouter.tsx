import { TourListPage } from './pages/TourListPage';
import { TourDetailPage } from './pages/TourDetailPage';
import { TourNameChangePage } from './pages/TourNameChangePage';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const AppRouter = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<TourListPage />} />
				<Route path="/tours/:tour_id" element={<TourDetailPage />} />
				<Route
					path="/tours/:tour_id/name-change"
					element={<TourNameChangePage />}
				/>
			</Routes>
		</BrowserRouter>
	);
};

export default AppRouter;
