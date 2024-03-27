import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'
import LoginPage from './components/LoginPage'
import RegisterPage from './components/RegisterPage'
import ErrorPage from './components/ErrorPage'

function App() {

  return (
    <Router>
      <div>
        <Routes>
          <Route exact path='/login' element={<LoginPage />}/>
          <Route exact path='/register' element={<RegisterPage />}/>
          <Route path='*' element={<ErrorPage/>}/>
        </Routes>
      </div>
    </Router>
  )
}

export default App
