import React, { useState, useEffect, useContext } from 'react';
import SideBar from '../../UI/SideBar/SideBar';
import Table from '../../UI/Table/Table';
import Card from '../../UI/Card/Card';

import { authContext } from '../../../context/authContext';

import classes from './Shop.module.css';

const Shop = () => {
	const { token } = useContext(authContext);
	const [items, setItems] = useState([]);

	const [isMsg, setIsMsg] = useState(false);
	const [messageTitle, setMessageTitle] = useState(null);
	const [messageContent, setMessageContent] = useState(null);
	const [error, setError] = useState(false);

	useEffect(() => {
		fetch(`${window.url}/api/locker`, {
			method: 'GET',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
		})
			.then((response) => response.json())
			.then((data) => {
				console.log('hi',(data));
				setItems(data);
			})
			.catch((error) => console.error(error));
	}, [token]);

	const handlePayment = (ID) => {
		console.log(ID);
		// execute
		fetch(`${window.url}/api/user/locker`, {
			method: 'POST',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				'locker_id': ID,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					return response.text().then((text) => {
						throw new Error(text);
					});
				}
				return response.json();
			})
			.then((data) => {
				setIsMsg(true);
				setMessageTitle('Thành công');
				setMessageContent('Bạn đã đăng ký tủ thành công!!!');
			})
			.catch((err) => {
				setIsMsg(true);
				const errorMessage = JSON.parse(err.message).error;
				setMessageTitle('Lỗi !!!');
				setError(true);
				setMessageContent(errorMessage);
				console.log(errorMessage);
			});
	};
	const handleCard = () => {
		setIsMsg(false);
		window.location.reload();
	};

	const columns = [
		{ field: 'id', header: 'ID' },
		{ field: 'avail', header: 'Trạng thái tủ' },
		{ field: 'coord', header: 'Vị trí tủ' },
		{ field: 'action', header: 'Action', content: 'Đăng ký' },
	];
	return (
		<div>
			{isMsg && (
				<Card
					className={`${classes.popup} ${error ? 'error' : 'success'}`}
					handleCard={handleCard}
					title={messageTitle}
				>
					<div className={classes.content}>
						{error ? (
							<i className='material-symbols-outlined'>error</i>
						) : (
							<i className='material-symbols-outlined'>check_circle</i>
						)}

						<div>{messageContent}</div>
					</div>
				</Card>
			)}
			{isMsg && <div className={classes.overlay} />}
			<SideBar currentIndex={2}>
				<Table data={items} columns={columns} handlePayment={handlePayment} />
			</SideBar>
		</div>
	);
};
export default Shop;
