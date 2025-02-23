import { useState, useEffect, useRef } from "react";
import { Menu, X } from "lucide-react";
import gsap from "gsap";
import { useAuth } from "../context/AuthProvider";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);
  const navbarRef = useRef(null);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    gsap.fromTo(
      navbarRef.current,
      { opacity: 0, y: -20 },
      { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }
    );
  }, []);

  useEffect(() => {
    if (isOpen) {
      gsap.fromTo(menuRef.current, { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4 });
    } else {
      gsap.to(menuRef.current, { opacity: 0, y: -20, duration: 0.3 });
    }
  }, [isOpen]);

  const handleLogout = () => {
    logout();
    toast.info("Logged out successfully! 👋"); // ✅ Logout Toast
    navigate("/login");
  };

  return (
    <nav ref={navbarRef} className="bg-white shadow-md p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold text-[#f73408]">
          <img src="/logo.png" alt="Logo" className="h-10 w-auto" />
        </div>

        <div className="hidden md:flex space-x-6">
          <a href="/home" className="text-gray-800 hover:text-[#f73408] font-medium">Home</a>
          <a href="/sales" className="text-gray-800 hover:text-[#f73408] font-medium">Sales</a>
          <a href="/stitching" className="text-gray-800 hover:text-[#f73408] font-medium">Stitching</a>
          <a href="/billing" className="text-gray-800 hover:text-[#f73408] font-medium">Billing</a>
        </div>

        {user ? (
          <button onClick={handleLogout} className="hidden md:block px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700">
            Logout
          </button>
        ) : (
          <a href="/login" className="hidden md:block px-4 py-2 bg-[#f73408] text-white rounded-lg hover:bg-[#d62806]">
            Login
          </a>
        )}

        <button className="md:hidden text-gray-800" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      <div ref={menuRef} className={`md:hidden flex flex-col items-center mt-4 space-y-4 ${isOpen ? "block" : "hidden"}`}>
        <a href="/home" className="text-gray-800 hover:text-[#f73408] font-medium">Home</a>
        <a href="/sales" className="text-gray-800 hover:text-[#f73408] font-medium">Sales</a>
        <a href="/stitching" className="text-gray-800 hover:text-[#f73408] font-medium">Stitching</a>
        <a href="/billing" className="text-gray-800 hover:text-[#f73408] font-medium">Billing</a>
        {user ? (
          <button onClick={handleLogout} className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700">Logout</button>
        ) : (
          <a href="/login" className="px-4 py-2 bg-[#f73408] text-white rounded-lg hover:bg-[#d62806]">Login</a>
        )}
      </div>
    </nav>
  );
}
