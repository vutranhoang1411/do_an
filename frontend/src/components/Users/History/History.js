import React, { useState, useEffect, useContext } from 'react';
import SideBar from '../../UI/SideBar/SideBar';
import { authContext } from '../../../context/authContext';

import classes from './History.module.css';

const UserLocker = () => {
	const { token } = useContext(authContext);
	const [paymentArray, setPaymentArray] = useState([]);

	useEffect(() => {
		fetch(`${window.url}/api/user/payment`, {
			method: 'GET',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
		})
			.then((response) => response.json())
			.then((data) => {
				setPaymentArray(data);
			})
			.catch((error) => console.error(error));
	}, [token]);

	return (
		<SideBar currentIndex={3}>
			<div className={classes.container}>
				<table className={classes.table}>
					<thead>
						<tr>
							<th>ID tủ</th>
							<th>ID khách hàng</th>
							<th>Ngày thuê</th>
							<th>Thời gian thuê</th>
							<th>Phương thức thanh toán</th>
							<th>Phí</th>
						</tr>
					</thead>
					<tbody>
						{paymentArray.map((d, index) => (
							<tr key={index}>
								<td>{d.id}</td>
								<td>{d.customerid}</td>
								<td>{d.rentdate}</td>
								<td>{d.duration} days</td>
								<td>{d.paymentmethod}</td>
								<td>{d.fee} VND</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</SideBar>
	);
};
export default UserLocker;
