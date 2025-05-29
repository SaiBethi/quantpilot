import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'text-blue-600' : 'text-gray-600 hover:text-blue-600';
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-blue-600">📈 QuantPilot</span>
          </Link>
          
          <div className="hidden md:flex space-x-8">
            <Link to="/" className={`${isActive('/')} transition-colors duration-200 font-medium`}>
              Home
            </Link>
            <Link to="/dashboard" className={`${isActive('/dashboard')} transition-colors duration-200 font-medium`}>
              Dashboard
            </Link>
            <Link to="/ai-insights" className={`${isActive('/ai-insights')} transition-colors duration-200 font-medium`}>
              AI Insights
            </Link>
            <Link to="/about" className={`${isActive('/about')} transition-colors duration-200 font-medium`}>
              About
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;