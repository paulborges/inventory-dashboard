import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar(){
    const navigate = useNavigate();
    const location = useLocation();
    const {user} = useAuth();

    const links = [
        {path: '/dashboard', label: 'Dashboard'},
        {path: '/products', label: 'Products'},
        {path: '/sales', label: 'Sales'},
        ...(user?.role==='admin'
            ?[{path:'/reports',label:'Reports'}]
            :[])
        ];
    return(
        <div className="sidebar">
            <div className="sidebar-brand">
                <span>Inventory Pro</span>
            </div>
            <nav className="sidebar-nav">
                {links.map(link=>(
                    <button
                    key = {link.path}
                    className={`sidebar-link ${location.pathname===link.path?'active':''}`}
                    onClick={()=>navigate(link.path)}
                    >
                    <span>{link.label}</span>
                    </button>
                ))}
            </nav>
            <div className="sidebar-user">
                <p className="sidebar-user-name">{user?.name}</p>
                <span className={`role-badge ${user?.role}`}>
                    {user?.role}
                </span>
            </div>
        </div>
    );
}

export default Sidebar;