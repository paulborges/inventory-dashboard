import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { loginUser } from "../services/api";

function LoginPage(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState('');

    const {login} = useAuth();
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        setError('');
        setLoading(true);

        try{
            const data = await loginUser(email,password);
            login(data.token,data.user);
            navigate('/dashboard');
        }catch (err){
            setError(err.message);
        }finally{
            setLoading(false);
        }
    }

    return(
        <div className="login-page">
            <div className="login-card">
                <div className="login-header">
                    <h1>Inventory Pro</h1>
                    <p>Business Made Simple</p>
                </div>
                {error &&(
                    <div className="error-banner">
                        {error}
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Enter your email" required/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" required/>
                    </div>
                    <button type="submit" className="btn-primary" disabled={loading}>{loading ? 'Logging in....': 'Login'}</button>
                </form>
                <div className="demo-credentials">
                    <p><strong>Demo Account:</strong></p>
                    <p>Admin: admin@demo.com</p>
                    <p>Staff: staff@demo.com</p>
                    <p>Password: admin123/staff123</p>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;

