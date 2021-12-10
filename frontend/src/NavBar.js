import Navbar from 'react-bootstrap/Navbar'
import Container from 'react-bootstrap/Container'
import {Nav, NavDropdown, Form, FormControl, Button} from 'react-bootstrap'
import React, {useEffect, useState} from 'react'
import {toQueryString} from './utils'
import config, {updateConfig} from './config'

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function updateEngine(e, setEngine){
    const engine = e.target.text
    setEngine(engine);
    updateConfig(true, engine);
}

function handleSearch(e, query){
  console.log(e)
  const url = window.location.origin + '/search?'+ toQueryString({q: query});
  window.location.replace(url)
}

function NavigationBar(){
    const [query, setQuery] = useState('');
    const [engine, setEngine] = useState(config.engine)
    return (<Navbar bg="dark" variant="dark">
    <Container>
      <Navbar.Brand href="/">Origin Finder</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="graph">Graph</Nav.Link>
          <NavDropdown title={engine} id="basic-nav-dropdown">
            <NavDropdown.Item onClick={(e) => {updateEngine(e, setEngine)}}>reddit</NavDropdown.Item>
            <NavDropdown.Item onClick={(e) => {updateEngine(e, setEngine)}}>twitter</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item >extra</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Form className="d-flex" onSubmit={(e)=>{handleSearch(e, query);e.preventDefault();}}>
        <FormControl
          type="search"
          placeholder="Search"
          className="me-2"
          aria-label="Search"
          onChange={(e)=>{setQuery(e.target.value);console.log(e.target.value)}}
          submit={(e)=>{handleSearch(e, query);e.preventDefault();}}
        />
        <Button id="navbar-submit" variant="outline-success" onClick={(e)=>{handleSearch(e, query)}}>Search</Button>
      </Form >
      </Navbar.Collapse>
    </Container>
  </Navbar>)
}

export default NavigationBar;