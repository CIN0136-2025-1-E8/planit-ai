import React, { useState } from 'react';
import styles from '../styles/AuthPage.module.css';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const loginUser = async () => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha }),
      });
      const data = await response.json();
      console.log('Login success:', data);
    } catch (err) {
      console.error('Erro ao fazer login:', err);
    }
  };

  return (
    <div className={styles.formSection}>
      <h2>Entre na sua conta!</h2>
      <button className={styles.googleBtn}>
        <img src="/google-icon.svg" alt="Google" />
        Entrar com Google
      </button>
      <p className={styles.divider}><hr />Ou<hr /></p>
      <input type="email" placeholder="Digite seu Email..." value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Digite sua Senha..." value={senha} onChange={e => setSenha(e.target.value)} />
      <a href="#" className={styles.forgot}>Esqueceu sua senha?</a>
      <button onClick={loginUser} className={styles.loginBtn}>Login</button>
    </div>
  );
};

export default LoginForm;
