import React, { useState } from 'react';
import Button from '../Button/Button';
import classes from './NavBar.module.css';
function NavBar(props) {
	const [isClicked, setIsClicked] = useState(false);
	const clickedHandle = () => {
		setIsClicked(!isClicked);
	};
	return (
		<div className={classes.container}>
			<nav className={classes.nav}>
				<a href='/'>
					<span className='material-symbols-outlined'>home</span>
				</a>
				<div>
					<ul
						className={
							isClicked
								? `${classes.navbar} ${classes.active}`
								: `${classes.navbar}`
						}
					>
						{/* <li>
							<a className={classes.active} href='index.html'>
								Home
							</a>
						</li>
						<li>
							<a href='index.html'>Shop</a>
						</li>
						<li>
							<a href='index.html'>About</a>
						</li>
						<li>
							<a href='index.html'>Contact</a>
						</li> */}

						<Button className='btn gre' onClick={props.isSignUp}>
							Get Started
						</Button>
					</ul>
				</div>
				<div className={classes.mobile}>
					<span className='material-symbols-outlined' onClick={clickedHandle}>
						{isClicked ? 'close' : 'menu'}
					</span>
				</div>
			</nav>
			<div className={classes.content}>{props.children}</div>
		</div>
	);
}

export default NavBar;
