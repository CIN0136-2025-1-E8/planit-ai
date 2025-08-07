import React from 'react';
import styles from '../styles/AuthPage.module.css';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

const AuthPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <img src="/planet-icon.svg" alt="Planit Logo" className={styles.logo} />
        <h1 className={styles.title}>Planit</h1>
        <div className={styles.forms}>
          <LoginForm />
          <hr />
          <RegisterForm />
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
