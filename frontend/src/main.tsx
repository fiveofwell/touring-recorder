import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { setupLeafletIcons } from './lib/leaflet';
import AppRouter from './AppRouter';

setupLeafletIcons();

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<AppRouter />
	</StrictMode>,
);
