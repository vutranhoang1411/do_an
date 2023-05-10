import React, { useState } from 'react';
import NavBar from '../UI/NavBar/NavBar';
import Button from '../UI/Button/Button';
import SignUp from '../Users/SignUp/SignUp';
import LogIn from '../Users/LogIn/LogIn';

import styles from './Home.module.css';

function Home(props) {
	const [isSignUp, setIsSignUp] = useState(false);
	const [isLogIn, setIsLogIn] = useState(false);

	const changeSignUp = () => {
		setIsSignUp(true);
		setIsLogIn(false);
	};
	const goBackHandle = () => {
		setIsSignUp(false);
		setIsLogIn(false);
	};
	const changeLogIn = () => {
		setIsSignUp(false);
		setIsLogIn(true);
	};

	return (
		<div>
			{isSignUp && <SignUp goBack={goBackHandle} logIn={changeLogIn} />}
			{isLogIn && (
				<LogIn
					goBack={goBackHandle}
					signUp={changeSignUp}
				/>
			)}

			<div
				className={`${styles.home} ${
					isSignUp || isLogIn ? styles.disabled : ''
				}`}
			>
				<NavBar isSignUp={changeSignUp}>
					<h1>Bắt đầu với chúng tôi từ hôm nay</h1>
					<Button className='btn gre' onClick={changeSignUp}>
						Get Started Now
					</Button>
				</NavBar>
			</div>
		</div>
	);
}

export default Home;
