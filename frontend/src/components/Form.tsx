/* eslint-disable @typescript-eslint/no-unused-vars */
// src/components/Formulario.tsx

import React from 'react';
import './form.css';
import { fetchOpponentsList } from '../services/oppponents'; 
import { fetchSquadsList } from '../services/squads';


const getSquadsOptions = async () => {
  try{
    const { squads } = await fetchSquadsList();

    if (!squads.length){
      return;
    }
    const squadOptions = squads.map((squad)=>{
        return(
          <option key={squad} value={squad}>{squad}</option>
        )
    })
    return squadOptions

  } catch {
    console.log("Erro ao consultar a API.")
  }


}

const squadOptions = await getSquadsOptions()

const getOpponentOptions = async () => {
  try{
    const { opponents } = await fetchOpponentsList();

    if (!opponents.length){
      return;
    }

    const opponentOptions = opponents.map((opponent)=>{
        return(
          <option key={opponent} value={opponent}>{opponent}</option>
        )
    })
    return opponentOptions
  } catch{
    console.log("Erro ao consultar API")
  }
}

const opponentOptions = await getOpponentOptions()

const Formulario = () =>{

  // TODO add return from Predicition.tsx and call fetchMatchPrediction
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Formulário enviado!');
  };

  return (
    <>
    <form className="form" onSubmit={handleSubmit}>
      
      <select defaultValue="">
        <option value="" disabled>Selecione o Mando de Campo</option>
          <option value="visitor" >Visitante</option>
          <option value="home" >Mandante</option>
      </select>

      <select defaultValue="">
        <option value="" disabled>Selecione a Formação do seu time</option>
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