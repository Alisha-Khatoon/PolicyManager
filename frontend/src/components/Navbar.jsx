import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-sm py-3">
      {" "}
      {/* Added py-3 for vertical padding */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {" "}
          {/* Added items-center for vertical alignment */}
          <div className="flex items-center">
            <Link
              to="/dashboard"
              className="text-2xl font-extrabold text-gray-900 mr-8"
            >
              {" "}
              {/* Increased text size, bolder font, added right margin */}
              Policy Manager
            </Link>
            {user && (
              <div className="hidden md:flex md:space-x-8">
                {" "}
                {/* md:ml-6 removed to allow mr-8 on title */}
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Dashboard
                </Link>
                <Link
                  to="/dashboard?action=upload"
                  className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Upload Policy
                </Link>
              </div>
            )}
          </div>
          <div className="flex items-center space-x-4">
            {user && (
              <span className="text-gray-700">{user.name || user.email}</span>
            )}
            <button
              onClick={logout}
              className="px-4 py-2 text-sm text-white bg-red-600 rounded-md hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
