// src/components/Formulario.tsx
import React from 'react';
import './form.css';

const Formulario = () =>{
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Formulário enviado!');
  };

  return (
    <>
    <form className="form" onSubmit={handleSubmit}>
      <input type="text" placeholder="Nome" />
      <input type="email" placeholder="Email" />
      
      <select defaultValue="">
        <option value="" disabled>Selecione o Gênero</option>
        <option value="masculino">Masculino</option>
        <option value="feminino">Feminino</option>
        <option value="outro">Outro</option>
      </select>

      <select defaultValue="">
        <option value="" disabled>Selecione o País</option>
        <option value="br">Brasil</option>
        <option value="us">Estados Unidos</option>
        <option value="pt">Portugal</option>
      </select>

      <button type="submit">Enviar</button>
    </form>
    </>

  );
};

export default Formulario;