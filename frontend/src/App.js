import React, { useState, useEffect } from 'react';
import { Routes, Route  } from 'react-router-dom';

import { authContext } from './context/authContext';
import Home from './components/Home/Home';
import Shop from './components/Users/Shop/Shop';
import Info from './components/Users/Info/Info';
import History from './components/Users/History/History';
import NotFound from './components/NotFound/NotFound';
import UserLocker from './components/Users/UserLocker/UserLocker';

import './App.css';

function App() {
	const [success, setSuccess] = useState(null);
	const [token, setToken] = useState('');

	useEffect(() => {
		const storedToken = sessionStorage.getItem('token');
		if (storedToken) {
			setToken(storedToken);
			setSuccess(true);
		} else {
			setSuccess(false);
		}
	}, []);

	return (
		<authContext.Provider value={{ success, setSuccess, token, setToken }}>
			<Routes>
				{success ? (
					<Route path='/' element={<Info />} />
				) : (
					<Route path='/' element={<Home />} />
				)}
				{success && <Route path='/userLocker' element={<UserLocker />} />}
				{success && <Route path='/shop' element={<Shop />} />}
				{success && <Route path='/history' element={<History />} />}

				{success != null && <Route path='*' element={<NotFound />} />}
			</Routes>
		</authContext.Provider>
	);
}

export default App;
