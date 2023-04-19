import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';

import './index.css';
import App from './App';

window.url = "http://localhost:5001";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		{/* <AuthProvider> */}
			<BrowserRouter>
				<App />
			</BrowserRouter>
		{/* </AuthProvider>+ */}
	</React.StrictMode>
);
