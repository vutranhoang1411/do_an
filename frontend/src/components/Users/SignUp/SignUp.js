import React, { useState, useRef } from 'react';
import classes from './SignUp.module.css';
import Button from '../../UI/Button/Button';
import Card from '../../UI/Card/Card';
import Wrapper from '../../Helpers/Wrapper';

const SignUp = (props) => {
	const name = useRef();
	const email = useRef();
	const password = useRef();

	const [errMsg, setErrMsg] = useState('');
	const [isSuccess, setIsSuccess] = useState(false);

	const signUpHandler = async (e) => {
		e.preventDefault();
		console.log(name.current.value);
		fetch(`${window.url}/api/user/create`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				name: name.current.value,
				email: email.current.value,
				password: password.current.value,
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
				// setIsMsg(true);
				// setMessageTitle('Thành công');
				// setMessageContent('Bạn đã đăng ký thành công!!!');
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
					className={classes.popup}
					handleCard={handleCard}
					title={'Thành công'}
				>
					<div className={classes.content}>
						<i className='material-symbols-outlined'>check_circle</i>
						<div>Bạn đã đăng ký thành công</div>
					</div>
				</Card>
			)}

			{!isSuccess && (
				<Wrapper>
					<div className={classes.left_side}>
						<div className={classes.logo}>Lockers</div>
						<div className={classes.logIn}>
							<div> Bạn đã có tài khoản</div>
							<Button className='btn-outline' onClick={props.logIn}>
								Đăng nhập
							</Button>
						</div>
					</div>
					<div className={classes.right_side}>
					<div className={classes.ico_back} onClick={props.goBack}>
							<span className='material-symbols-outlined'>close</span>
						</div>
						<div className={classes.title}> Account Signup</div>
						<div className={classes.describe}>
							Trở thành thành viên của chúng tôi.
						</div>
						<form className={classes.input} onSubmit={signUpHandler}>
							<label htmlFor='username'>Họ và Tên</label>
							<input id='username' type='text' ref={name} />
							<label htmlFor='age'>Địa chỉ email</label>
							<input id='age' type='email' ref={email} />
							<label htmlFor='password'>Mật khẩu</label>
							<input id='password' type='password' ref={password} />
							<div className={classes.errMsg}> {errMsg}</div>

							<div className={classes.goLogIn}>
								Bạn đã có tài khoản?
								<span onClick={props.logIn}>Đăng nhập ngay</span>
							</div>
							<Button className={`${'btn red'} ${classes.btn_back}`} onClick={props.goBack}>
								Close
							</Button>
							<Button className={`${'btn gre'} ${classes.btn_signUp}`} type='submit'>
								Đăng Ký
							</Button>
						</form>
					</div>
				</Wrapper>
			)}
		</div>
	);
};
export default SignUp;
