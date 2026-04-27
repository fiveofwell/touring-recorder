import { TourListPage } from './pages/TourListPage';
import { TourDetailPage } from './pages/TourDetailPage';
import { TourNameChangePage } from './pages/TourNameChangePage';
import { DeviceManagementPage } from './pages/DeviceManagementPage';
import { DeviceCreatePage } from './pages/DeviceCreatePage';
import {
	BrowserRouter,
	Navigate,
	Outlet,
	Route,
	Routes,
} from 'react-router-dom';
import LoginPage from './pages/LoginPage';

const RequireAuth = () => {
	const token = localStorage.getItem('access_token');

	if (!token) {
		alert('再度ログインしてください');
		return <Navigate to="/" replace />;
	}

	return <Outlet />;
};

const AppRouter = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<LoginPage />} />
				<Route element={<RequireAuth />}>
					<Route path="/tours" element={<TourListPage />} />
					<Route
						path="/tours/:client_tour_id/points"
						element={<TourDetailPage />}
					/>
					<Route
						path="/tours/:client_tour_id/edit"
						element={<TourNameChangePage />}
					/>
					<Route path="/devices" element={<DeviceManagementPage />} />
					<Route path="/devices/new" element={<DeviceCreatePage />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
};

export default AppRouter;
