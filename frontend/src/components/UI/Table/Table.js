import React from 'react';
import classes from './Table.module.css';

import Button from '../Button/Button';

const Table = (props) => {
	const transmitID = (id) => {
		props.handlePayment(id);
	};
	return (
		<table className={classes.table}>
			<tbody>
				<tr key='head'>
					{props.columns.map((head) => {
						if (head.header !== 'Action') {
							return <th key={head.header}>{head.header}</th>;
						} else {
							return (
								<th key='action' className={classes.rightFormat}>
									{head.header}
								</th>
							);
						}
					})}
				</tr>
				{props.data.map((row, index) => (
					<tr key={index}>
						{props.columns.map((col) => {
							if (col.field === 'avail') {
								return (
									<td
										key={row[col.field]}
										className={
											row[col.field] ? classes.availTrue : classes.availFalse
										}
									>
										{row[col.field] ? 'Sẵn sàng' : 'Chưa sẵn sàng'}
									</td>
								);
							} else if (col.field !== 'action') {
								return <td key={row[col.field]}>{row[col.field]}</td>;
							} else {
								return (
									<td key='button' className={classes.rightFormat}>
										<Button
											className='btn gre'
											onClick={() => transmitID(row['id'])}
										>
											{col.content}
										</Button>
									</td>
								);
							}
						})}
					</tr>
				))}
			</tbody>
		</table>
	);
};
export default Table;
