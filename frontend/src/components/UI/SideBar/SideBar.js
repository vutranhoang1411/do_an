import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';

import { authContext } from '../../../context/authContext';
import Button from '../Button/Button';

import classes from './SideBar.module.css';

const Sidebar = (props) => {
	const { setSuccess, setToken } = useContext(authContext);
	const [navCollapse, setNavCollapse] = useState('');
	const storedName = sessionStorage.getItem('name');


	const SidebarItems = [
		{
			name: 'Thông tin cá nhân',
			route: '/',
			icon: 'person',
		},
		{
			name: 'Tủ của tôi',
			route: '/userLocker',
			icon: 'store',
		},
		{
			name: 'Đăng ký tủ',
			route: '/shop',
			icon: 'shopping_cart',
		},
		{
			name: 'Lịch sử giao dịch',
			route: '/history',
			icon: 'history',
		},
	];
	const isActive = (index) => {
		if (index === props.currentIndex) {
			return classes.active;
		} else {
			return '';
		}
	};
	const LogOut = () => {
		setSuccess(false);
		setToken('');
		sessionStorage.removeItem('token');
		window.location.href = '/';
	};
	return (
		<div className={classes.container}>
			<div className={classes.sidebar_content}>
				<div
					className={`${classes.sidebar_container} ${
						navCollapse ? classes.navCollaps : ''
					}`}
				>
					<div className={classes.nav_title}>
						<h2>Lockers</h2>
					</div>
					<div className={classes.nav_info}>
						<i>
							<span className='material-symbols-outlined'>account_circle</span>
						</i>
						<h6>{storedName}</h6>
					</div>
					{SidebarItems.map((item, index) => (
						<Link
							to={item.route}
							className={`${classes.nav_option} ${isActive(index)} `}
							key={index}
						>
							<i className='material-symbols-outlined' title={item.name}>
								{item.icon}
							</i>
							<h4> {item.name} </h4>
						</Link>
					))}

					<div className={classes.logout} onClick={LogOut}>
						<span className='material-symbols-outlined'>
							power_settings_new
						</span>
						<h4>Log Out</h4>
					</div>
				</div>
			</div>
			<div className={classes.main}>
				<nav className={classes.nav}>
					<div className={classes.logo}>
						<i onClick={(e) => setNavCollapse(!navCollapse)}>
							<span className='material-symbols-outlined'>menu</span>
						</i>
					</div>

					<Button className='btn org'>
						<Link to='/shop' className={classes.nav_register} key='register'>
							<span className='material-symbols-outlined'>edit</span>
							Đăng ký tủ
						</Link>
					</Button>
					<ul></ul>
				</nav>
				<div className={classes.content}>{props.children}</div>
			</div>
		</div>
	);
};

export default Sidebar;
