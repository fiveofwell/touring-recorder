import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { TourListPage } from './tour-list-page';
import { TourDetailPage } from './tour-detail-page';
import { TourNameChangePage } from './tour-name-change-page';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { setupLeafletIcons } from './lib/leaflet';

setupLeafletIcons();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<TourListPage />} />
	<Route path='/tours/:tour_id' element={<TourDetailPage />} />
	<Route path='/tours/:tour_id/name-change' element={<TourNameChangePage />} />

	
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
