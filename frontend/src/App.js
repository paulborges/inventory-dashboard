import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import './App.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoadingSpinner from './components/LoadingSpinner';
import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ProductsPage from './pages/ProductsPage';
import SalesPage from './pages/SalesPage';
import ReportsPage from './pages/ReportsPage';


function ProtectedRoute({children}){
  const {user, loading} = useAuth();

  if(loading) return <LoadingSpinner/>;

  if(!user) return <Navigate to = '/login'/>

  return children;
}

function AdminRoute({children}){
  const {user} = useAuth();

  if(user?.role !=='admin') return <Navigate to ='/dashboard'/>

  return children;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>

          <Route path ='/login' element = {<LoginPage/>}/>

          <Route path = '/' element = {
            <ProtectedRoute>
              <Layout/>
            </ProtectedRoute>
          }>
            <Route index element = {<Navigate to = '/dashboard'/>}/>
            <Route path = 'dashboard' element ={<DashboardPage/>}/>
            <Route path = 'products' element ={<ProductsPage/>}/>
            <Route path = 'sales' element ={<SalesPage/>}/>

            <Route path= 'reports' element={
              <AdminRoute>
                <ReportsPage/>
              </AdminRoute>
            }/>
          </Route>

          <Route path = '*' element = {<Navigate to= '/dashboard'/>}/>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
