import { createContext, useContext, useState, useEffect } from "react";
import { getCurrUser } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({children}){
    const[user, setUser] = useState(null);
    const[loading,setLoading] = useState(true);

    useEffect(()=>{
        async function checkToken() { 
            const token = localStorage.getItem('token');

            if (token){
                try{
                    const userData = await getCurrUser();
                    setUser(userData);
                }catch{
                    localStorage.removeItem('token');
                    setUser(null);
                }
            }
            setLoading(false);
        }
    checkToken();
},[]);

function login (token,userData){
    localStorage.setItem('token',token);
    setUser(userData);
}

function logout (token,userData){
    localStorage.removeItem('token');
    setUser(null);
}

return(
    <AuthContext.Provider value={{user, loading, login, logout}}>
        {children}    
    </AuthContext.Provider>
);
}

export function useAuth(){
    return useContext(AuthContext);
}