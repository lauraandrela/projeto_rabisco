import Headerb from '../components/Headerb'
import Titulo from '../components/Titulo'
import CardList from '@/components/CardList'
import { getProdutos } from '@/services/apirabisco'
import { useState, useEffect } from 'react'

export default function produtos() {
   const [produtos,setProdutos] = useState([])

   async function buscaProdutos() {
    try {
        const data = await getProdutos()
        console.log(data)
        setProdutos(data)
    } catch (error){
        console.error('Erro ao buscar produtos:', error)
    }
   }
   
   useEffect(function (){
    buscaProdutos()
   },[])

    return (
        <>
            <Headerb />
            <Titulo texto="Conheça nossos produtos!" />
            <CardList produtos={produtos} />
        </>
    )
}