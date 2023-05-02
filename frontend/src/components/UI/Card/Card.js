import React from 'react';
import classes from './Card.module.css';

const Card = (props) => {
	const stylesMessage = props.className.includes('success') ? classes.success : classes.error;
	const disappearButton = props.disappearButton ? classes.disappear : '';
	return (
		// <div className={props.className}>
			<div className={`${classes.card} ${props.className} ${stylesMessage}`}>
				<div className={classes.card_contents}>
					<div className={classes.title}>{props.title}</div>
					<div className={classes.content} >
						{props.children}
					</div>
					<button className={`${classes.btn} ${disappearButton}`} onClick={props.handleCard}>OK</button>
				</div>
			</div>
	);
};

export default Card;
