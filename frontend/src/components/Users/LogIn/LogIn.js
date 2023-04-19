import React, { useState, useRef } from 'react';

import Button from '../../UI/Button/Button';
import Card from '../../UI/Card/Card';
import Wrapper from '../../Helpers/Wrapper';

import classes from './LogIn.module.css';

const LogIn = (props) => {
	const emailInputRef = useRef();
	const passwordInputRef = useRef();
	const [errMsg, setErrMsg] = useState('');
	const [isSuccess, setIsSuccess] = useState(false);

	const logInHandler = async (e) => {
		e.preventDefault();
		fetch(`${window.url}/api/user/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				email: emailInputRef.current.value,
				password: passwordInputRef.current.value,
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
				setIsSuccess(true);
				const token = data.token;
				console.log(token);
				sessionStorage.setItem('token', token);
			})
			.catch((err) => {
				const errorMessage = JSON.parse(err.message).error;
				setErrMsg(errorMessage);
				console.log(errorMessage);
			});
	};

	const handleCard = () => {
		window.location.reload();
	};

	return (
		<div className={classes.container}>
			{isSuccess && (
				<Card
					className={`${classes.popup} ${'success'}`}
					handleCard={handleCard}
					title={'Thành công'}
				>
					<div className={classes.content}>
						<i className='material-symbols-outlined'>check_circle</i>
						<div>Bạn đã đăng nhập thành công</div>
					</div>
				</Card>
			)}

			{!isSuccess && (
				<Wrapper>
					<div className={classes.left_side}>
						<div className={classes.logo}>Lockers</div>
						<div className={classes.logIn}>
							<div> Bạn chưa có tài khoản</div>
							<Button className='btn-outline' onClick={props.signUp}>
								Đăng ký
							</Button>
						</div>
					</div>
					<div className={classes.right_side}>
						<div className={classes.ico_back} onClick={props.goBack}>
							<span className='material-symbols-outlined'>close</span>
						</div>
						<div className={classes.title}> Account LogIn</div>
						<div className={classes.describe}>Đăng nhập ngay</div>
						<form className={classes.input} onSubmit={logInHandler}>
							<label htmlFor='age'>Địa chỉ email</label>
							<input
								className={errMsg ? classes.error : ''}
								id='age'
								type='email'
								ref={emailInputRef}
							/>
							<label htmlFor='password'>Mật khẩu</label>
							<input className={errMsg ? classes.error : ''} id='password' type='password' ref={passwordInputRef} />
							<div className={classes.errMsg}> {errMsg}</div>
							<div className={classes.goLogIn}>
								Bạn chưa có tài khoản?
								<span onClick={props.signUp}>Đăng ký ngay</span>
							</div>
							<Button
								className={`${'btn red'} ${classes.btn_back}`}
								onClick={props.goBack}
							>
								Close
							</Button>
							<Button
								className={`${'btn gre'} ${classes.btn_logIn}`}
								type='submit'
							>
								Đăng Nhập
							</Button>
						</form>
					</div>
				</Wrapper>
			)}
		</div>
	);
};
export default LogIn;
