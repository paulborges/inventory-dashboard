import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar(){
    const {user, logout} = useAuth();
    const location = useLocation();
    const navigate = useNavigate();

    function getPageTitle(){
        const path = location.pathname;
        if (path === '/dashboard') return 'Dashboard';
        if (path === '/products') return 'Products';
        if (path === '/sales') return 'Sales';
        if (path === '/reports') return 'Reports';
        return 'InventoryPro';
    }

    function handleLogout(){
        logout();
        navigate('/login');
    }
    
    return(
        <div className="navbar">
            <h2 className="navbar-title">{getPageTitle()}</h2>
            <div className="navbar-user">
                <span className="navbar-username">{user?.name}</span>
                <span className={`role-badge ${user?.role}`}>
                    {user?.role}
                </span>
                <button className="btn-logout" onClick={handleLogout}>Logout</button>
            </div>
        </div>
    );
}

export default Navbar;