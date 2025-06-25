import { NavLink } from "react-router-dom";

export default function Sidebar({ onUploadClick }) {
  return (
    <div className="w-64 bg-white shadow-md">
      <div className="p-4 space-y-1">
        <button
          onClick={onUploadClick}
          className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
        >
          Upload Policy
        </button>
        <NavLink
          to="/dashboard/policies"
          className={({ isActive }) =>
            `block px-4 py-2 rounded-md ${
              isActive
                ? "bg-blue-50 text-blue-600"
                : "text-gray-700 hover:bg-gray-100"
            }`
          }
        >
          My Policies
        </NavLink>
      </div>
    </div>
  );
}
