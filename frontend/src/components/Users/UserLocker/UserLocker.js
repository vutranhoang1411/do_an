import React, { useState, useEffect, useContext } from 'react';
import SideBar from '../../UI/SideBar/SideBar';
import Table from '../../UI/Table/Table';
import Card from '../../UI/Card/Card';
import Wrapper from '../../Helpers/Wrapper';
import { authContext } from '../../../context/authContext';

import classes from './UserLocker.module.css';

const UserLocker = () => {
	const { token } = useContext(authContext);

	const [items, setItems] = useState([]);
	const [closed, setClosed] = useState(true);
	const [id, setId] = useState(null);
	const [selectedOption, setSelectedOption] = useState(null);
	const [isMsg, setIsMsg] = useState(false);
	const [messageTitle, setMessageTitle] = useState(null);
	const [messageContent, setMessageContent] = useState(null);
	const [error, setError] = useState(false);

	const handleOptionChange = (event) => {
		setSelectedOption(event.target.value);
	};
	useEffect(() => {
		fetch(`${window.url}/api/user/locker`, {
			method: 'GET',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
		})
			.then((response) => response.json())
			.then((data) => {
				setItems(data);
			})
			.catch((error) => console.error(error));
	}, [token]);

	const handlePayment = (ID) => {
		setId(ID);
		setClosed(false);
	};
	const executePayment = () => {
		console.log(id);
		console.log(selectedOption);

		// execute
		fetch(`${window.url}/api/user/payment`, {
			method: 'POST',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				locker_id: id,
				method: selectedOption,
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
				setMessageTitle('Thành công');
				console.log(data);
				const msgSuccessPayment = data;
				setMessageContent(
					<Wrapper>
						<i className='material-symbols-outlined'>check_circle</i>
						<ul className={classes.list}>
							<li>
								Id hoá đơn: <span>{msgSuccessPayment.id} </span>
							</li>
							<li>
								Id tủ: <span>{msgSuccessPayment.cabinetid}</span>
							</li>
							<li>
								Id khách hàng: <span>{msgSuccessPayment.customerid}</span>
							</li>
							<li>
								Ngày thuê: <span>{msgSuccessPayment.rentdate}</span>
							</li>
							<li>
								Thời gian thuê: <span>{msgSuccessPayment.duration} </span>
							</li>
							<li>
								Phương thức thanh toán:{' '}
								<span>{msgSuccessPayment.paymentmethod}</span>
							</li>
							<li>
								Thuế: <span>{msgSuccessPayment.fee}</span>
							</li>
						</ul>
					</Wrapper>
				);
				// setIsSuccessPayment(true);
				setIsMsg(true);
			})
			.catch((err) => {
				setIsMsg(true);
				const errorMessage = JSON.parse(err.message).error;
				setMessageTitle('Lỗi !!!');
				setMessageContent(
					<Wrapper>
						<i class='material-symbols-outlined'>error</i>
						<div className={classes.content}>{errorMessage}</div>
					</Wrapper>
				);
				setError(true);
				console.log(errorMessage);
			});
	};
	const handleCard = () => {
		// setIsSuccessPayment(false);
		setIsMsg(false);
		window.location.reload();
	};
	const columns = [
		{ field: 'id', header: 'ID' },
		{ field: 'start_time', header: 'Thời gian bắt đầu thuê' },
		{ field: 'coord', header: 'Vị trí tủ' },
		{ field: 'action', header: 'Action', content: 'Thanh toán' },
	];
	return (
		<div>
			{isMsg && (
				<Card
					className={`${classes.popup} ${error ? 'error' : 'success'}`}
					handleCard={handleCard}
					title={messageTitle}
				>
					<div className={classes.content}>{messageContent}</div>
				</Card>
			)}
			{isMsg && <div className={classes.overlay} />}
			<SideBar currentIndex={1}>
				<Table data={items} columns={columns} handlePayment={handlePayment} />
				<div className={`${classes.payment} ${closed ? classes.closed : ''}`}>
					<div className={classes.header}>
						Đơn hàng của bạn
						<i onClick={(e) => setClosed(!closed)}>
							<span className='material-symbols-outlined'>close</span>
						</i>
					</div>
					<div className={classes.title}>Hình thức thanh toán</div>
					<div className={classes.selected}>
						<input
							type='radio'
							name='payment'
							value='card'
							onChange={handleOptionChange}
						/>
						<label htmlFor='card'>Thẻ ATM/Thẻ nội địa</label>
						<br />
						<input
							type='radio'
							name='payment'
							value='momo'
							onChange={handleOptionChange}
						/>
						<label htmlFor='momo'>Ví điện tử momo</label>
						<br />
						<input
							type='radio'
							name='payment'
							value='zalopay'
							onChange={handleOptionChange}
						/>
						<label htmlFor='javascript'>Ví điện tử zalopay</label>
						<br />
						<button onClick={executePayment}>Thanh toán</button>
					</div>
				</div>
			</SideBar>
		</div>
	);
};
export default UserLocker;
