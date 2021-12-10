import logo from './logo.svg';
import './App.css';
import {toQueryString, keywordToQueryString} from './utils'
import config from './config'
import { useTable, useSortBy } from 'react-table'
import React, {useEffect, useState} from 'react'
import styled from 'styled-components'

import 'bootstrap/dist/css/bootstrap.min.css';

import BTable from 'react-bootstrap/Table';

const searxURL = config.searxURL

const Styles = styled.div`

table {
  border-spacing: 0;
  border: 1px solid black;

  tr {
    :last-child {
      td {
        border-bottom: 0;
      }
    }
  }

  th,
  td {
    margin: 0;
    padding: 0.5rem;
    border-bottom: 1px solid black;
    border-right: 1px solid black;

    :last-child {
      border-right: 0;
    }
  }
}
`

function getMemoCompatibleHeader(col){
    const columns = [];
    for(const id of col){
      const res = {
        Header: id,
        accessor: id.replace(' ', '')
    }
        if(id == 'metric'){
          res['sortType'] = 'basic';
        }
        columns.push(res)
    }
    return columns;
}

async function request(url, req_params= {
    referrer: '',
    mode: 'cors',
    method: 'GET'
  }){
    const res = await fetch(url, req_params);
    return await res.json();
}

async function getNewPosts(params){
  const res = await request(searxURL + '?' + toQueryString(params), null);
  return res;
}

function getParams(raw_params){
    const params = {
        q: raw_params.get('q'),
        engines: config.engine
    }
    return {...params, ...raw_params}
}

async function streamRoutine(params){
    const res = await getNewPosts(params);
    const results = res['results']
    console.log(results)
    for (const [i, result] of results.entries()){
        var url = window.location.pathname + '?' + toQueryString({
            q: keywordToQueryString(result['keywords']),
            engines: params['engines']
        })
        result['similar'] = url;

        url =  '/user?' + toQueryString({
            q: result['author'],
            engines: result['engine']
        })
        result['user'] = url;
    }
    console.log(results)
    return results;
}



function Search() {
    const [results, setResults] = useState([]);
    const raw_params = new URLSearchParams(window.location.search);
    const params = getParams(raw_params);
    const col = ['title', 'content', 'publishedDate', 'url', 'metric', 'veracity', 'similar', 'user']

    const columns = React.useMemo(()=>getMemoCompatibleHeader(col), []);
    const data = React.useMemo(()=>results, [results])

    React.useEffect(async ()=>{
            const results = await streamRoutine(params);
            for(const result of results){
                result['user'] = <a href={result['user']}>user</a>
                result['similar'] = <a href={result['similar']}>similar</a>
                result['metric'] = (result['metric']/10**6).toFixed(2);
            }
            setResults(results)
    },[])
    // streamRoutine(params)
    // .then((res)=> setResults(res))
    console.log(columns);
    console.log(data);

    const tableInstance = useTable({ columns, data }, useSortBy)
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
      } = tableInstance
      
      return  (
          <Styles>
        <BTable striped bordered hover size="sm"  variant="dark" {...getTableProps()}>
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                  <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                    <span>{column.isSorted ? (column.isSortedDesc ? ' 🔽' : ' 🔼') : ''}</span>
                    {column.render('Header')}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row, i) => {
              prepareRow(row)
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => {
                    return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                  })}
                </tr>
              )
            })}
          </tbody>
        </BTable>
        </Styles>
      )
}


export default Search;
