// src/components/Formulario.tsx
import React from 'react';
import './form.css';
// import { fetchOpponentsList } from '../services/opponent'; 
// import { fetchFormationList } from '../services/formation'; 

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
        <option value="Home">Home</option>
        <option value="Visitor">Visitor</option>
      </select>

      <select defaultValue="">
        <option value="" disabled>Select the opponent</option>
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