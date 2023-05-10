import React from 'react';
import { Link } from 'react-router-dom';

import classes from './NotFound.module.css'
const NotFound = () => (
  <div className={classes.notFound}>
    <div className={classes.code}>404</div>
    <div className={classes.text}>Not Found</div>

    <Link to="/" className={classes.link}>
      Go Home
    </Link>
  </div>
);

export default NotFound;
