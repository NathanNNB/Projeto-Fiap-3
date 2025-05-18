/* eslint-disable @typescript-eslint/no-unused-vars */
// src/components/Formulario.tsx

import React from 'react';
import './form.css';
import { fetchOpponentsList } from '../services/oppponents'; 
import { fetchSquadsList } from '../services/squads';

console.log(fetchSquadsList)
console.log(fetchOpponentsList)

const getSquadsOptions = async () => {
  let squads;
  try{
    squads = await fetchSquadsList();
    if (!squads.length){
      return;
    }
    const squadOptions = squads.map((squad)=>{
        return(
          <option value={squad}>`${squad}`</option>
        )
    })
    return squadOptions

  } catch {
    console.log("Erro ao consultar a API.")
  }


}

const squadOptions = await getSquadsOptions()

const getOpponentOptions = async () => {
  let opponent
  try{
    const opponent = await fetchOpponentsList();

    if (!opponent.length){
      return;
    }

    const opponentOptions = opponent.map((opponent)=>{
        return(
          <option value={opponent}>`${opponent}`</option>
        )
    })
    return opponentOptions
  } catch{
    console.log("Erro ao consultar API")
  }
}

const opponentOptions = await getOpponentOptions()

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
        <option value="" disabled>Selecione a Formação</option>
        {squadOptions}
      </select>

      <select defaultValue="">
        <option value="" disabled>Selecione o oponente</option>
        {opponentOptions}
      </select>

      <button type="submit">Enviar</button>
    </form>
    </>

  );
};

export default Formulario;