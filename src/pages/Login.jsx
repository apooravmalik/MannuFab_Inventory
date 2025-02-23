import { useState, useEffect, useRef } from "react";
import { useAuth } from "../context/AuthProvider";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import gsap from "gsap";
import MannuFabLogo from "../assets/Mannu_Fab_Logo.jpeg";
import { toast } from "sonner";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { setUser } = useAuth();
  const navigate = useNavigate();
  const formRef = useRef(null);

  // GSAP Animation on Page Load
  useEffect(() => {
    gsap.fromTo(
      formRef.current,
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }
    );
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Login failed");
      }

      // ✅ Store user details in localStorage
      localStorage.setItem("access_token", data.session.access_token);
      localStorage.setItem("user_email", data.user.email);
      localStorage.setItem("user_id", data.user.id);

      // ✅ Update Auth Context
      setUser({ id: data.user.id, email: data.user.email, token: data.session.access_token });

      toast.success("Login successful! 🎉"); // ✅ Success toast

      navigate("/home");
    } catch (err) {
      setError(err.message);
      toast.error(`Login failed: ${err.message}`); // ✅ Error toast
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div ref={formRef} className="flex flex-col justify-center items-center h-screen">
      {/* Logo */}
      <div className="mb-6">
        <img src={MannuFabLogo} alt="Mannu Fab Logo" className="w-auto h-auto mx-auto" />
      </div>

      {/* Login Form */}
      <form className="bg-white p-6 rounded shadow-md w-80" onSubmit={handleLogin}>
        <h2 className="text-2xl font-semibold mb-4 text-center">Login</h2>
        {error && <p className="text-red-500 text-center">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          className="border p-2 w-full mb-3"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            className="border p-2 w-full mb-3"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="button"
            className="absolute inset-y-0 right-3 flex items-center text-gray-600"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
          </button>
        </div>

        <button
          className="w-full bg-[#f73408] text-white p-2 rounded hover:bg-[#d62806] flex justify-center items-center"
          disabled={loading}
        >
          {loading ? (
            <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              ></path>
            </svg>
          ) : (
            "Login"
          )}
        </button>
      </form>

      {/* Footer Info */}
      <div className="text-center mt-6">
        <p>
          Follow us on{" "}
          <a
            href="https://www.instagram.com/mannu_fab/"
            className="text-[#f73408] font-semibold"
            target="_blank"
            rel="noopener noreferrer"
          >
            Instagram
          </a>
        </p>
        <p>📞 Contact: <span className="font-semibold">9811549906</span></p>
        <p>
          Developed by{" "}
          <a
            href="https://apoorav-malik.netlify.app/"
            className="text-[#f73408] font-semibold"
            target="_blank"
            rel="noopener noreferrer"
          >
            Apoorav Malik
          </a>
        </p>
      </div>
    </div>
  );
}
