import logo from './logo.svg';
import './App.css';
import {toQueryString, keywordToQueryString} from './utils'
import New from './new.js'
import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";
import User from './user';
import Search from './search';
import NavigationBar from './NavBar';
import Graph from './Graph'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div>
    <NavigationBar />
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<New />} />
      <Route path="user" element={<User />} />
      <Route path="search" element={<Search />} />
      <Route path="graph" element={<Graph />} />
    </Routes>
  </BrowserRouter>
  </div>
  );
}

export default App;
