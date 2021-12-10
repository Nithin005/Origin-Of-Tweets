import logo from './logo.svg';
import './App.css';
import {toQueryString, keywordToQueryString} from './utils'
import config from './config'
import { useTable } from 'react-table'
import React, {useEffect, useState} from 'react'
import styled from 'styled-components'
import ReactJson from 'react-json-view'

async function request(url, req_params= {
    referrer: '',
    mode: 'cors',
    method: 'GET'
  }){
    const res = await fetch(url, req_params);
    return await res.json();
}

function getParams(raw_params){
    const params = {
        q: raw_params.get('q'),
        engines: raw_params.get('engines') || config.engine
    }
    return {...params, ...raw_params}
}

async function fetchUserDataRoutine(params){
    const url = config.searxURL+ '/user'+ '?' + toQueryString(params)
    console.log(url)
    const res = await request(url);
    return res;
}

function User(){
    const raw_params = new URLSearchParams(window.location.search);
    const params = getParams(raw_params);
    const [result, setResult] = useState({});
    useEffect(async()=>{
        const result = await fetchUserDataRoutine(params)
        setResult(result);
    }, [])

    return <ReactJson src={result} />;
}

export default User