import React, { useState } from 'react';
import styles from '../styles/AuthPage.module.css';

const RegisterForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [nome, setNome] = useState('');
  const [senha, setSenha] = useState('');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const registerUser = async () => {
    setError('');
    setSuccess(false);

    if (!email || !nome || !senha) {
      setError('Por favor, preencha todos os campos.');
      return;
    }

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, nome, senha }),
      });

      if (!response.ok) {
        throw new Error('Falha no cadastro');
      }

      const data = await response.json();
      console.log('Cadastro feito:', data);
      setSuccess(true);

      // Limpa o formulário
      setEmail('');
      setNome('');
      setSenha('');
    } catch (err) {
      setError('Erro ao se cadastrar. Tente novamente.');
      console.error(err);
    }
  };

  return (
    <div className={styles.formSection}>
      <h2>Crie sua conta Plannit!</h2>
      <input
        type="email"
        placeholder="Digite seu Email..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        placeholder="Digite seu Nome de Usuário..."
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="password"
        placeholder="Digite sua Senha..."
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
      />
      {error && <p style={{ color: 'red', fontSize: 12 }}>{error}</p>}
      {success && <p style={{ color: 'green', fontSize: 12 }}>Cadastro realizado com sucesso!</p>}
      <button onClick={registerUser} className={styles.registerBtn}>
        Cadastre-se
      </button>
    </div>
  );
};

export default RegisterForm;