import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';

import SideBar from '../../UI/SideBar/SideBar';
import Button from '../../UI/Button/Button';
import Wrapper from '../../Helpers/Wrapper';
import Card from '../../UI/Card/Card';

import { authContext } from '../../../context/authContext';

import classes from './Info.module.css';

const Info = () => {
	const { token } = useContext(authContext);
	const [data, setData] = useState({ name: '', email: '', password: '' });
	const [image, setImage] = useState({});

	const [showPassword, setShowPassword] = useState(false);
	const [showUpdateImg, setShowUpdateImg] = useState(false);

	const [isMsg, setIsMsg] = useState(false);
	const [messageTitle, setMessageTitle] = useState(null);
	const [messageContent, setMessageContent] = useState(null);
	const [error, setError] = useState(false);

	const togglePasswordVisibility = () => {
		setShowPassword(!showPassword);
	};
	const toggleUpdateImg = () => {
		setShowUpdateImg(!showUpdateImg);
	};
	const handleCard = () => {
		window.location.reload();
	};
	const handleImage = (e) => {
		console.log(e.target.files);
		setImage(e.target.files[0]);
	};
	const closeUpdateImg = () => {
		setShowUpdateImg(false);
	};
	const inputChangedHandler = (event) => {
		return event.target.value;
	};
	// Update image
	const 	headers = {
			'authorization': `${token}`,
		};

	const handleAPI = () => {
		const formData = new FormData();
		formData.append('img', image);
		axios
			.post(`${window.url}/api/user/img`, formData, {headers})
			.then((response) => {
				if (response.status === 200) {
					setIsMsg(true);
					setShowUpdateImg(false);
					setMessageTitle('Thành công');
					setMessageContent('Bạn đã cập nhật ảnh thành công!!!');
				} else {
					return response.text().then((text) => {
						throw new Error(text);
					});
				}
			})
			.catch((err) => {
				setIsMsg(true);
				setShowUpdateImg(false);
				const errorMessage = err.response.data.error;
				setMessageTitle('Lỗi !!!');
				setError(true);
				setMessageContent(errorMessage);
			});
	};
	useEffect(() => {
		fetch(`${window.url}/api/user`, {
			method: 'GET',
			headers: {
				authorization: `${token}`,
				'Content-Type': 'application/json',
			},
		})
			.then((response) => response.json())
			.then((dataJson) => {
				sessionStorage.setItem('name', dataJson.name);

				setData(dataJson);
			})
			.catch((error) => console.error(error));
	}, [token]);

	return (
		<Wrapper>
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
			{showUpdateImg && (
				<Card
					className={classes.updateImg}
					title={'Update Image'}
					disappearButton={true}
				>
					<div>
						<input type='file' name='file' onChange={handleImage} />
						<Button
							className={`${'btn red'} ${classes.btnUpdateImg}`}
							onClick={closeUpdateImg}
						>
							Close
						</Button>
						<Button
							className={`${'btn gre'} ${classes.btnUpdateImg}`}
							onClick={handleAPI}
						>
							Submit
						</Button>
					</div>
				</Card>
			)}

			{(isMsg || showUpdateImg) && <div className={classes.overlay} />}
			<SideBar currentIndex={0}>
				<div className={classes.container}>
					<div className={classes.title}> Thông tin cá nhân </div>
					<div className={classes.image}>
						{data.photo && <img src={`${window.url}/public/img/${data.photo}`} alt='profile' />}
						<div className={classes.update} onClick={toggleUpdateImg}>
							Upload ảnh
						</div>
					</div>
					<div className={classes.input}>
						<label htmlFor='username'>Họ và Tên</label>
						<input
							id='username'
							type='text'
							value={data.name}
							onChange={(event) => inputChangedHandler(event)}
						/>
						<label htmlFor='age'>Địa chỉ email</label>
						<input
							id='age'
							type='email'
							value={data.email}
							onChange={(event) => inputChangedHandler(event)}
						/>
						<label htmlFor='password'>Mật khẩu</label>
						<input
							id='password'
							type={showPassword ? 'text' : 'password'}
							value={data.password}
							onChange={(event) => inputChangedHandler(event)}
						/>

						<Button className='btn gre' onClick={togglePasswordVisibility}>
							{showPassword ? 'Ẩn' : 'Hiện'}
						</Button>
					</div>
				</div>
			</SideBar>
		</Wrapper>
	);
};
export default Info;
