import SideBar from '../../UI/SideBar/SideBar';
import Button from '../../UI/Button/Button';

import classes from './Info.module.css';

const Info = (props) => {
	return (
		<SideBar currentIndex={1}>
			<div className={classes.content}>
				<div className={classes.left_content}>
					<div className={classes.title}> Thông tin cá nhân </div>
					<form className={classes.input}>
						<label htmlFor='username'>Họ và Tên</label>
						<input id='username' type='text' value={'Nhật Thiên'} />

						<label htmlFor='age'>Địa chỉ email</label>
						<input id='age' type='email' value={'thien@gmail.com'} />

						<label htmlFor='phone'>Số điện thoại</label>
						<input id='phone' type='tel' value={'0123'} />

						<label htmlFor='gender'>Giới tính</label>
						<input id='gender' type='text' />

						<label htmlFor='password'>Mật khẩu</label>
						<input id='password' type='password' value={'0123'} />

						<Button className='btn' type='submit'>
							Cập nhật
						</Button>
					</form>
				</div>
				<div className={classes.right_content}>
						<div className={classes.title}> Thông tin ngân hàng </div>
						<form className={classes.input}>
							<label htmlFor='bank'>Ngân hàng</label>
							<input id='bank' type='text' value={'Nhật Thiên'} />

							<label htmlFor='name'>Tên tài khoản</label>
							<input id='name' type='text' value={'thien@gmail.com'} />

							<label htmlFor='num'>Số tài khoản</label>
							<input id='num' type='tel' value={'0123'} />

							<Button className='btn' type='submit'>
								Thêm tài khoản
							</Button>
						</form>
					</div>
			</div>
		</SideBar>
	);
};
export default Info;
